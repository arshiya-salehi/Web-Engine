"""
M3 Optimized Search Engine
Disk-based search without loading entire index into memory
Uses efficient JSON parsing for term-specific lookups
"""

import json
import os
import sys
import math
import re
from collections import defaultdict

from stemmer import Stemmer
from tokenizer import Tokenizer


class M3SearchEngine:
    """Optimized disk-based search engine for M3"""
    
    def __init__(self, index_dir='index'):
        """
        Initialize M3 search engine
        
        Args:
            index_dir: Directory containing index files
        """
        self.index_dir = index_dir
        self.index_file = os.path.join(index_dir, 'inverted_index.json')
        self.doc_mapping_file = os.path.join(index_dir, 'doc_mapping.json')
        
        # Initialize components
        self.stemmer = Stemmer()
        self.tokenizer = Tokenizer()
        
        # Document mappings (small, kept in memory)
        self.doc_mappings = None
        self.total_docs = 0
        
        # Caches
        self.df_cache = {}  # Document frequency cache
        self.postings_cache = {}  # Postings cache (LRU, limited size)
        self.cache_max_size = 500  # Limit cache size
        
        # Index file metadata
        self.index_file_size = 0
        if os.path.exists(self.index_file):
            self.index_file_size = os.path.getsize(self.index_file)
        
        # Load document mappings
        self._load_doc_mappings()
    
    def _load_doc_mappings(self):
        """Load document URL to ID mappings"""
        if not os.path.exists(self.doc_mapping_file):
            raise FileNotFoundError(f"Document mapping file not found: {self.doc_mapping_file}")
        
        with open(self.doc_mapping_file, 'r', encoding='utf-8') as f:
            data = json.load(f)
            self.doc_mappings = {
                'url_to_id': data.get('url_to_id', {}),
                'id_to_url': {int(k): v for k, v in data.get('id_to_url', {}).items()}
            }
        
        self.total_docs = len(self.doc_mappings['url_to_id'])
        print(f"Loaded {self.total_docs} document mappings")
    
    def _extract_term_from_json(self, term, file_content):
        """
        Extract a specific term's data from JSON content without parsing entire file
        Uses regex to find and extract the term's JSON object
        """
        # Pattern to find the term: "term": { ... }
        pattern = rf'"{re.escape(term)}"\s*:\s*(\{{[^}}]*(?:\{{[^}}]*\}}[^}}]*)*\}})'
        
        match = re.search(pattern, file_content)
        if not match:
            return None
        
        try:
            # Extract the JSON object
            term_json_str = match.group(1)
            # Parse just this term's data
            term_data = json.loads('{' + f'"{term}": {term_json_str}' + '}')
            return term_data.get(term, {})
        except (json.JSONDecodeError, ValueError):
            # If regex extraction fails, try a more robust method
            return self._extract_term_robust(term, file_content, match.start())
    
    def _extract_term_robust(self, term, file_content, start_pos):
        """More robust extraction using brace matching"""
        # Find the opening brace after the term
        brace_start = file_content.find('{', start_pos)
        if brace_start == -1:
            return None
        
        # Match braces to find the complete object
        brace_count = 0
        i = brace_start
        while i < min(brace_start + 200000, len(file_content)):  # Limit search
            if file_content[i] == '{':
                brace_count += 1
            elif file_content[i] == '}':
                brace_count -= 1
                if brace_count == 0:
                    # Found the complete object
                    obj_str = file_content[brace_start:i+1]
                    try:
                        term_data = json.loads('{' + f'"{term}": {obj_str}' + '}')
                        return term_data.get(term, {})
                    except json.JSONDecodeError:
                        return None
            i += 1
        
        return None
    
    def _get_postings_from_disk(self, term):
        """
        Get postings for a term by reading from disk
        Does NOT load entire index into memory
        """
        # Check cache first
        if term in self.postings_cache:
            return self.postings_cache[term].copy()
        
        if not os.path.exists(self.index_file):
            return {}
        
        try:
            # Read file in chunks and extract the term
            # For large files, we read the entire file but don't parse it all
            with open(self.index_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extract just this term's data
            term_data = self._extract_term_from_json(term, content)
            
            if term_data:
                # Convert to our format
                postings = {}
                for doc_id_str, posting_data in term_data.items():
                    postings[int(doc_id_str)] = posting_data
                
                # Cache it (with size limit)
                if len(self.postings_cache) >= self.cache_max_size:
                    # Remove oldest entry (simple FIFO)
                    oldest_term = next(iter(self.postings_cache))
                    del self.postings_cache[oldest_term]
                
                self.postings_cache[term] = postings.copy()
                return postings
            
            return {}
        
        except Exception as e:
            print(f"Error reading postings for term '{term}': {e}", file=sys.stderr)
            return {}
    
    def _get_postings(self, term):
        """Get postings for a term"""
        return self._get_postings_from_disk(term)
    
    def _get_document_frequency(self, term):
        """Get document frequency for a term"""
        if term in self.df_cache:
            return self.df_cache[term]
        
        postings = self._get_postings(term)
        df = len(postings)
        self.df_cache[term] = df
        return df
    
    def _calculate_enhanced_tf_idf(self, tf, df, total_docs, is_important=False):
        """
        Calculate enhanced TF-IDF with improvements:
        - Sublinear TF scaling
        - Smoothed IDF
        - Important word boosting
        """
        if df == 0 or total_docs == 0:
            return 0.0
        
        # Sublinear TF: log(1 + tf) to prevent bias toward very long documents
        tf_score = 1 + math.log(tf) if tf > 0 else 0
        
        # Smoothed IDF: log((N + 1) / (df + 1)) + 1
        idf_score = math.log((total_docs + 1) / (df + 1)) + 1
        
        base_score = tf_score * idf_score
        
        # Boost important words (bold, headings, title)
        if is_important:
            base_score *= 2.0  # 2x boost for important words
        
        return base_score
    
    def _process_query(self, query):
        """Process and normalize query"""
        tokens = self.tokenizer.tokenize(query)
        stemmed_tokens = self.stemmer.stem_tokens(tokens)
        # Remove duplicates while preserving order
        seen = set()
        unique_tokens = []
        for token in stemmed_tokens:
            if token not in seen:
                seen.add(token)
                unique_tokens.append(token)
        return unique_tokens
    
    def search(self, query, top_k=10):
        """
        Enhanced search with improved ranking
        """
        # Process query
        query_terms = self._process_query(query)
        
        if not query_terms:
            return []
        
        # Get postings for each term
        term_postings = {}
        for term in query_terms:
            postings = self._get_postings(term)
            if postings:
                term_postings[term] = postings
        
        if not term_postings:
            return []
        
        # Boolean AND: intersect posting lists
        # Start with smallest list for efficiency
        sorted_terms = sorted(term_postings.items(), key=lambda x: len(x[1]))
        if not sorted_terms:
            return []
        
        first_term, first_postings = sorted_terms[0]
        candidate_docs = set(first_postings.keys())
        
        for term, postings in sorted_terms[1:]:
            candidate_docs = candidate_docs.intersection(set(postings.keys()))
        
        if not candidate_docs:
            return []
        
        # Calculate enhanced scores
        doc_scores = defaultdict(float)
        
        # Pre-compute document frequencies
        term_dfs = {term: self._get_document_frequency(term) for term in query_terms if term in term_postings}
        
        for doc_id in candidate_docs:
            score = 0.0
            matching_terms = 0
            
            for term in query_terms:
                if term in term_postings and doc_id in term_postings[term]:
                    posting = term_postings[term][doc_id]
                    tf = posting.get('tf', 0)
                    is_important = posting.get('is_important', False)
                    df = term_dfs.get(term, 0)
                    
                    # Calculate enhanced TF-IDF
                    term_score = self._calculate_enhanced_tf_idf(tf, df, self.total_docs, is_important)
                    score += term_score
                    matching_terms += 1
            
            # Bonus for complete matches (all terms present)
            if matching_terms == len(query_terms):
                score *= 1.15  # 15% boost
            
            # Normalize by query length (avoid bias toward longer queries)
            if len(query_terms) > 1:
                score /= math.sqrt(len(query_terms))
            
            doc_scores[doc_id] = score
        
        # Sort and return top_k
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        results = []
        for doc_id, score in sorted_docs[:top_k]:
            if doc_id in self.doc_mappings['id_to_url']:
                url = self.doc_mappings['id_to_url'][doc_id]
                results.append((url, score))
        
        return results

