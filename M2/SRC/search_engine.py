"""
Search Engine Module
Implements disk-based search with boolean AND queries and tf-idf ranking
"""

import json
import os
import sys
import math
from collections import defaultdict

# Import from local files (copied from shared directory)
from stemmer import Stemmer
from tokenizer import Tokenizer


class SearchEngine:
    """Disk-based search engine that reads from index files"""
    
    def __init__(self, index_dir='index'):
        """
        Initialize search engine
        
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
        
        # Cache for document frequencies (df) - will be computed on demand
        self.df_cache = {}
        
        # Cache for index data (loaded on first use)
        self.index_cache = None
        self.index_loaded = False
        
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
    
    def _load_index(self):
        """Load the entire index into memory (cached after first load)"""
        if self.index_loaded:
            return
        
        if not os.path.exists(self.index_file):
            raise FileNotFoundError(f"Index file not found: {self.index_file}")
        
        print("Loading index into memory...")
        try:
            with open(self.index_file, 'r', encoding='utf-8') as f:
                self.index_cache = json.load(f)
            self.index_loaded = True
            print(f"Index loaded: {len(self.index_cache)} unique terms")
        except Exception as e:
            print(f"Error loading index: {e}", file=sys.stderr)
            raise
    
    def _get_document_frequency(self, term):
        """
        Get document frequency (df) for a term
        Uses caching to avoid repeated lookups
        
        Args:
            term: Stemmed term to look up
            
        Returns:
            Number of documents containing this term
        """
        if term in self.df_cache:
            return self.df_cache[term]
        
        # Load index if not already loaded
        if not self.index_loaded:
            self._load_index()
        
        # Get document frequency from cached index
        if term in self.index_cache:
            df = len(self.index_cache[term])
            self.df_cache[term] = df
            return df
        else:
            self.df_cache[term] = 0
            return 0
    
    def _get_postings(self, term):
        """
        Get postings list for a term from the cached index
        
        Args:
            term: Stemmed term to look up
            
        Returns:
            Dictionary mapping doc_id (int) to posting data
        """
        # Load index if not already loaded
        if not self.index_loaded:
            self._load_index()
        
        if term in self.index_cache:
            # Convert string doc_ids to integers
            postings = {}
            for doc_id_str, posting_data in self.index_cache[term].items():
                postings[int(doc_id_str)] = posting_data
            return postings
        else:
            return {}
    
    def _calculate_tf_idf(self, tf, df, total_docs):
        """
        Calculate tf-idf score
        
        Args:
            tf: Term frequency in document
            df: Document frequency (number of documents containing term)
            total_docs: Total number of documents in corpus
            
        Returns:
            tf-idf score
        """
        if df == 0 or total_docs == 0:
            return 0.0
        
        # Use log-based tf-idf: tf * log(N / df)
        # Using log(1 + tf) for term frequency to avoid zero issues
        tf_score = 1 + math.log(tf) if tf > 0 else 0
        idf_score = math.log(total_docs / df) if df > 0 else 0
        
        return tf_score * idf_score
    
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
        Search for documents matching the query (boolean AND)
        
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
        # Get intersection of all posting lists
        first_term = list(term_postings.keys())[0]
        candidate_docs = set(term_postings[first_term].keys())
        
        for term in list(term_postings.keys())[1:]:
            candidate_docs = candidate_docs.intersection(set(term_postings[term].keys()))
        
        if not candidate_docs:
            return []
        
        # Calculate scores for each candidate document
        doc_scores = defaultdict(float)
        
        for doc_id in candidate_docs:
            score = 0.0
            
            for term in query_terms:
                if term in term_postings and doc_id in term_postings[term]:
                    posting = term_postings[term][doc_id]
                    tf = posting.get('tf', 0)
                    is_important = posting.get('is_important', False)
                    
                    # Get document frequency
                    df = self._get_document_frequency(term)
                    
                    # Calculate tf-idf
                    tf_idf = self._calculate_tf_idf(tf, df, self.total_docs)
                    
                    # Boost score if term is important
                    if is_important:
                        tf_idf *= 1.5  # Boost important words
                    
                    score += tf_idf
            
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

