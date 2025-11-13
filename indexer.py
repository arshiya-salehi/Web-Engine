"""
Indexer Module
Builds an inverted index from documents
"""

from collections import defaultdict
import json
import os


class InvertedIndex:
    """Inverted index data structure"""
    
    def __init__(self):
        # Index structure: {term: {doc_id: {'tf': count, 'is_important': bool}}}
        self.index = defaultdict(lambda: defaultdict(lambda: {'tf': 0, 'is_important': False}))
        self.doc_ids = {}  # Map from URL to doc_id
        self.doc_id_to_url = {}  # Reverse mapping
        self.next_doc_id = 0
    
    def add_document(self, url, tokens, important_tokens):
        """
        Add a document to the index
        
        Args:
            url: Document URL
            tokens: List of normal tokens
            important_tokens: List of important tokens
        """
        # Get or create doc_id for this URL
        if url not in self.doc_ids:
            doc_id = self.next_doc_id
            self.doc_ids[url] = doc_id
            self.doc_id_to_url[doc_id] = url
            self.next_doc_id += 1
        else:
            doc_id = self.doc_ids[url]
        
        # Create a set of important tokens for quick lookup
        important_set = set(important_tokens)
        
        # Count term frequencies for normal tokens
        token_counts = defaultdict(int)
        for token in tokens:
            token_counts[token] += 1
        
        # Count term frequencies for important tokens
        important_token_counts = defaultdict(int)
        for token in important_tokens:
            important_token_counts[token] += 1
        
        # Add all tokens to index
        all_tokens = set(tokens) | set(important_tokens)
        for token in all_tokens:
            tf_normal = token_counts.get(token, 0)
            tf_important = important_token_counts.get(token, 0)
            total_tf = tf_normal + tf_important
            
            # Mark as important if it appears in important tokens
            is_important = token in important_set or tf_important > 0
            
            # Update index
            self.index[token][doc_id] = {
                'tf': total_tf,
                'is_important': is_important
            }
    
    def get_num_documents(self):
        """Get the number of indexed documents"""
        return len(self.doc_ids)
    
    def get_num_unique_tokens(self):
        """Get the number of unique tokens in the index"""
        return len(self.index)
    
    def save_to_disk(self, output_dir='index'):
        """
        Save the index to disk as JSON
        
        Args:
            output_dir: Directory to save index files
        """
        os.makedirs(output_dir, exist_ok=True)
        
        # Save the main index
        index_file = os.path.join(output_dir, 'inverted_index.json')
        index_data = {}
        for term, postings in self.index.items():
            index_data[term] = {
                str(doc_id): posting_data 
                for doc_id, posting_data in postings.items()
            }
        
        with open(index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f, indent=2)
        
        # Save document mappings
        doc_mapping_file = os.path.join(output_dir, 'doc_mapping.json')
        with open(doc_mapping_file, 'w', encoding='utf-8') as f:
            json.dump({
                'url_to_id': self.doc_ids,
                'id_to_url': {str(k): v for k, v in self.doc_id_to_url.items()}
            }, f, indent=2)
        
        return index_file, doc_mapping_file
    
    def get_index_size_kb(self, output_dir='index'):
        """
        Get the size of the index on disk in KB
        
        Args:
            output_dir: Directory containing index files
        """
        total_size = 0
        index_file = os.path.join(output_dir, 'inverted_index.json')
        doc_mapping_file = os.path.join(output_dir, 'doc_mapping.json')
        
        if os.path.exists(index_file):
            total_size += os.path.getsize(index_file)
        if os.path.exists(doc_mapping_file):
            total_size += os.path.getsize(doc_mapping_file)
        
        return total_size / 1024.0  # Convert to KB

