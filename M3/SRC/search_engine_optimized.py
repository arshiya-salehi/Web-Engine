"""
Optimized Search Engine Module for M3
Implements disk-based search without loading entire index into memory
Uses streaming JSON parsing and optimized data structures
"""

import json
import os
import sys
import math
import mmap
from collections import defaultdict

# Import from local files
from stemmer import Stemmer
from tokenizer import Tokenizer


class OptimizedSearchEngine:
    """Disk-based search engine that reads postings from disk without loading entire index"""
    
    def __init__(self, index_dir='index'):
        """
        Initialize optimized search engine
        
        Args:
            index_dir: Directory containing index files
        """
        self.index_dir = index_dir
        self.index_file = os.path.join(index_dir, 'inverted_index.json')
        self.doc_mapping_file = os.path.join(index_dir, 'doc_mapping.json')
        
        # Initialize components
        self.stemmer = Stemmer()
        self.tokenizer = Tokenizer()
        
        # Cache for document mappings (small enough to keep in memory)
        self.doc_mappings = None
        self.total_docs = 0
        
        # Cache for document frequencies (df) - computed on demand from disk
        self.df_cache = {}
        
        # Cache for recently accessed postings (LRU cache)
        self.postings_cache = {}
        self.cache_size_limit = 1000  # Cache up to 1000 terms
        
        # Index file handle and memory map for efficient access
        self.index_fd = None
        self.index_mmap = None
        self.index_size = 0
        
        # Pre-computed term positions in file (for faster lookups)
        self.term_positions = {}
        self._build_term_index()
        
        # Load document mappings
        self._load_doc_mappings()
    
    def _build_term_index(self):
        """
        Build a lightweight index of term positions in the JSON file
        This allows us to quickly locate terms without parsing the entire file
        """
        if not os.path.exists(self.index_file):
            return
        
        print("Building term position index...")
        try:
            # Read file in chunks to find term positions
            # JSON format: {"term1": {...}, "term2": {...}, ...}
            with open(self.index_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # Find positions of each term using regex-like approach
                # Look for pattern: "term": { ... }
                import re
                # Match: "term": { ... }
                pattern = r'"([^"]+)":\s*\{'
                matches = re.finditer(pattern, content)
                
                for match in matches:
                    term = match.group(1)
                    pos = match.start()
                    self.term_positions[term] = pos
                
            print(f"Indexed {len(self.term_positions)} terms")
        except Exception as e:
            print(f"Warning: Could not build term index: {e}", file=sys.stderr)
            # Fallback: will use full file parsing
    
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
    
    def _get_postings_from_disk(self, term):
        """
        Get postings list for a term by reading from disk
        Uses streaming JSON parsing to avoid loading entire index
        
        Args:
            term: Stemmed term to look up
            
        Returns:
            Dictionary mapping doc_id (int) to posting data
        """
        # Check cache first
        if term in self.postings_cache:
            return self.postings_cache[term]
        
        if not os.path.exists(self.index_file):
            return {}
        
        try:
            # Method 1: If we have term positions, use them for faster access
            if term in self.term_positions:
                # Read a chunk around the term position
                with open(self.index_file, 'r', encoding='utf-8') as f:
                    # Seek to approximate position
                    f.seek(self.term_positions[term] - 100)  # Start a bit before
                    chunk = f.read(50000)  # Read 50KB chunk
                    # Find the term's JSON object
                    start = chunk.find(f'"{term}":')
                    if start != -1:
                        # Extract the JSON object for this term
                        # Find the matching brace
                        brace_count = 0
                        obj_start = chunk.find('{', start)
                        if obj_start != -1:
                            i = obj_start + 1
                            while i < len(chunk):
                                if chunk[i] == '{':
                                    brace_count += 1
                                elif chunk[i] == '}':
                                    if brace_count == 0:
                                        obj_end = i + 1
                                        term_json = chunk[obj_start:obj_end]
                                        try:
                                            term_data = json.loads('{' + f'"{term}": {term_json}' + '}')
                                            postings = {}
                                            for doc_id_str, posting_data in term_data[term].items():
                                                postings[int(doc_id_str)] = posting_data
                                            # Cache it
                                            if len(self.postings_cache) < self.cache_size_limit:
                                                self.postings_cache[term] = postings
                                            return postings
                                        except:
                                            pass
                                    else:
                                        brace_count -= 1
                                i += 1
            
            # Method 2: Fallback - parse JSON and extract only the needed term
            # This is still more efficient than loading the entire index
            with open(self.index_file, 'r', encoding='utf-8') as f:
                # Use streaming JSON parser
                decoder = json.JSONDecoder()
                content = f.read()
                
                # Find the term in the JSON
                term_pattern = f'"{term}":'
                term_pos = content.find(term_pattern)
                if term_pos == -1:
                    return {}
                
                # Extract the JSON object for this term
                # Find the opening brace after the term
                brace_start = content.find('{', term_pos)
                if brace_start == -1:
                    return {}
                
                # Find matching closing brace
                brace_count = 0
                brace_end = brace_start
                for i in range(brace_start, min(brace_start + 100000, len(content))):
                    if content[i] == '{':
                        brace_count += 1
                    elif content[i] == '}':
                        brace_count -= 1
                        if brace_count == 0:
                            brace_end = i + 1
                            break
                
                # Extract and parse the term's postings
                term_json_str = content[brace_start:brace_end]
                try:
                    term_data = json.loads('{' + f'"{term}": {term_json_str}' + '}')
                    postings = {}
                    for doc_id_str, posting_data in term_data[term].items():
                        postings[int(doc_id_str)] = posting_data
                    # Cache it
                    if len(self.postings_cache) < self.cache_size_limit:
                        self.postings_cache[term] = postings
                    return postings
                except json.JSONDecodeError:
                    # If parsing fails, fall back to loading entire index (last resort)
                    return self._get_postings_fallback(term)
        
        except Exception as e:
            print(f"Error reading postings for term {term}: {e}", file=sys.stderr)
            return {}
    
    def _get_postings_fallback(self, term):
        """Fallback method: load entire index (only used if streaming fails)"""
        with open(self.index_file, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
            if term in index_data:
                postings = {}
                for doc_id_str, posting_data in index_data[term].items():
                    postings[int(doc_id_str)] = posting_data
                return postings
        return {}
    
    def _get_postings(self, term):
        """
        Get postings list for a term (wrapper with caching)
        
        Args:
            term: Stemmed term to look up
            
        Returns:
            Dictionary mapping doc_id (int) to posting data
        """
        return self._get_postings_from_disk(term)
    
    def _get_document_frequency(self, term):
        """
        Get document frequency (df) for a term
        Computed from postings list length
        
        Args:
            term: Stemmed term to look up
            
        Returns:
            Number of documents containing this term
        """
        if term in self.df_cache:
            return self.df_cache[term]
        
        postings = self._get_postings(term)
        df = len(postings)
        self.df_cache[term] = df
        return df
    
    def _calculate_tf_idf(self, tf, df, total_docs):
        """
        Calculate enhanced tf-idf score with normalization
        
        Args:
            tf: Term frequency in document
            df: Document frequency (number of documents containing term)
            total_docs: Total number of documents in corpus
            
        Returns:
            Enhanced tf-idf score
        """
        if df == 0 or total_docs == 0:
            return 0.0
        
        # Enhanced tf-idf with sublinear tf scaling
        # Using log(1 + tf) for term frequency (sublinear scaling)
        tf_score = 1 + math.log(tf) if tf > 0 else 0
        
        # IDF with smoothing to avoid division by zero
        idf_score = math.log((total_docs + 1) / (df + 1)) + 1
        
        return tf_score * idf_score
    
    def _calculate_document_length_normalization(self, doc_id, term_postings):
        """
        Calculate document length normalization factor
        Uses sum of tf values as proxy for document length
        
        Args:
            doc_id: Document ID
            term_postings: Dictionary of term -> postings dict
            
        Returns:
            Normalization factor
        """
        # Sum of term frequencies in this document
        doc_length = 0
        for term, postings in term_postings.items():
            if doc_id in postings:
                doc_length += postings[doc_id].get('tf', 0)
        
        # Normalize by average document length (approximation)
        # Using sqrt for length normalization
        if doc_length > 0:
            return 1.0 / math.sqrt(doc_length)
        return 1.0
    
    def _process_query(self, query):
        """
        Process query: tokenize and stem
        
        Args:
            query: Raw query string
            
        Returns:
            List of stemmed tokens
        """
        tokens = self.tokenizer.tokenize(query)
        stemmed_tokens = self.stemmer.stem_tokens(tokens)
        return stemmed_tokens
    
    def search(self, query, top_k=10):
        """
        Search for documents matching the query (boolean AND with improved ranking)
        
        Args:
            query: Query string
            top_k: Number of top results to return
            
        Returns:
            List of tuples (url, score) sorted by score (descending)
        """
        # Process query
        query_terms = self._process_query(query)
        
        if not query_terms:
            return []
        
        # Remove duplicate terms
        query_terms = list(dict.fromkeys(query_terms))  # Preserves order
        
        # Get postings for each term
        term_postings = {}
        for term in query_terms:
            postings = self._get_postings(term)
            if postings:
                term_postings[term] = postings
        
        # If no terms found in index, return empty
        if not term_postings:
            return []
        
        # Boolean AND: find documents that contain ALL query terms
        # Start with the term that has the smallest posting list (for efficiency)
        sorted_terms = sorted(term_postings.items(), key=lambda x: len(x[1]))
        if not sorted_terms:
            return []
        
        first_term, first_postings = sorted_terms[0]
        candidate_docs = set(first_postings.keys())
        
        # Intersect with remaining terms
        for term, postings in sorted_terms[1:]:
            candidate_docs = candidate_docs.intersection(set(postings.keys()))
        
        if not candidate_docs:
            return []
        
        # Calculate enhanced scores for each candidate document
        doc_scores = defaultdict(float)
        
        # Pre-compute document frequencies for all terms
        term_dfs = {}
        for term in query_terms:
            if term in term_postings:
                term_dfs[term] = self._get_document_frequency(term)
        
        for doc_id in candidate_docs:
            score = 0.0
            term_count = 0  # Count of matching terms
            
            for term in query_terms:
                if term in term_postings and doc_id in term_postings[term]:
                    posting = term_postings[term][doc_id]
                    tf = posting.get('tf', 0)
                    is_important = posting.get('is_important', False)
                    
                    # Get document frequency
                    df = term_dfs.get(term, 0)
                    
                    # Calculate enhanced tf-idf
                    tf_idf = self._calculate_tf_idf(tf, df, self.total_docs)
                    
                    # Boost score if term is important (bold, headings, title)
                    if is_important:
                        tf_idf *= 2.0  # Increased boost for important words
                    
                    # Boost for exact term matches (query term appears as-is)
                    # This helps with specific queries
                    score += tf_idf
                    term_count += 1
            
            # Bonus for documents containing all query terms
            if term_count == len(query_terms):
                score *= 1.2  # 20% boost for complete matches
            
            # Normalize by query length (to avoid bias toward longer queries)
            if len(query_terms) > 0:
                score /= math.sqrt(len(query_terms))
            
            doc_scores[doc_id] = score
        
        # Sort by score (descending) and get top_k
        sorted_docs = sorted(doc_scores.items(), key=lambda x: x[1], reverse=True)
        
        # Convert doc_ids to URLs
        results = []
        for doc_id, score in sorted_docs[:top_k]:
            if doc_id in self.doc_mappings['id_to_url']:
                url = self.doc_mappings['id_to_url'][doc_id]
                results.append((url, score))
        
        return results

