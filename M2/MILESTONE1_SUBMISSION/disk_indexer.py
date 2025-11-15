"""
Disk-Based Indexer Module
Implements memory-efficient indexing with periodic disk offloading
Required for Algorithms and Data Structures Developer option
"""

from collections import defaultdict
import json
import os
import tempfile
import shutil


class DiskBasedIndexer:
    """Memory-efficient indexer that offloads to disk periodically"""
    
    def __init__(self, output_dir='index', max_docs_in_memory=10000):
        """
        Initialize disk-based indexer
        
        Args:
            output_dir: Directory to save index files
            max_docs_in_memory: Maximum documents to process before offloading
        """
        self.output_dir = output_dir
        self.max_docs_in_memory = max_docs_in_memory
        self.partial_index_dir = os.path.join(output_dir, 'partial_indexes')
        os.makedirs(self.partial_index_dir, exist_ok=True)
        
        # In-memory structures (will be periodically flushed)
        self.index = defaultdict(lambda: defaultdict(lambda: {'tf': 0, 'is_important': False}))
        self.doc_ids = {}
        self.doc_id_to_url = {}
        self.next_doc_id = 0
        self.docs_in_memory = 0
        self.partial_index_count = 0
        
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
        
        self.docs_in_memory += 1
        
        # Offload to disk if memory limit reached
        if self.docs_in_memory >= self.max_docs_in_memory:
            self._offload_to_disk()
    
    def _offload_to_disk(self):
        """Offload current in-memory index to disk as a partial index"""
        if len(self.index) == 0:
            return
        
        print(f"  Offloading partial index #{self.partial_index_count + 1} to disk... "
              f"({self.docs_in_memory} documents, {len(self.index)} unique tokens)")
        
        # Save partial index
        partial_index_file = os.path.join(
            self.partial_index_dir, 
            f'partial_index_{self.partial_index_count:03d}.json'
        )
        
        # Convert to JSON-serializable format
        index_data = {}
        for term, postings in self.index.items():
            index_data[term] = {
                str(doc_id): posting_data 
                for doc_id, posting_data in postings.items()
            }
        
        with open(partial_index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f)
        
        # Save partial doc mappings
        partial_mapping_file = os.path.join(
            self.partial_index_dir,
            f'partial_mapping_{self.partial_index_count:03d}.json'
        )
        
        with open(partial_mapping_file, 'w', encoding='utf-8') as f:
            json.dump({
                'url_to_id': self.doc_ids,
                'id_to_url': {str(k): v for k, v in self.doc_id_to_url.items()}
            }, f)
        
        self.partial_index_count += 1
        
        # Clear in-memory index (but keep doc mappings for final merge)
        self.index.clear()
        self.docs_in_memory = 0
    
    def finalize(self):
        """
        Finalize indexing: offload remaining data and merge all partial indexes
        """
        # Offload any remaining in-memory data
        if len(self.index) > 0:
            self._offload_to_disk()
        
        print(f"\nMerging {self.partial_index_count} partial indexes...")
        
        # Merge all partial indexes
        self._merge_partial_indexes()
        
        # Save final document mappings
        self._save_doc_mappings()
        
        # Clean up partial index files
        if os.path.exists(self.partial_index_dir):
            shutil.rmtree(self.partial_index_dir)
    
    def _merge_partial_indexes(self):
        """Merge all partial indexes into final index"""
        if self.partial_index_count == 0:
            # No partial indexes, save what we have in memory
            self._save_final_index()
            return
        
        # Load and merge all partial indexes
        merged_index = defaultdict(lambda: defaultdict(lambda: {'tf': 0, 'is_important': False}))
        
        for i in range(self.partial_index_count):
            partial_index_file = os.path.join(
                self.partial_index_dir,
                f'partial_index_{i:03d}.json'
            )
            
            print(f"  Loading partial index {i+1}/{self.partial_index_count}...")
            
            with open(partial_index_file, 'r', encoding='utf-8') as f:
                partial_index = json.load(f)
            
            # Merge into main index
            for term, postings in partial_index.items():
                for doc_id_str, posting_data in postings.items():
                    doc_id = int(doc_id_str)
                    # Merge postings (combine tf, keep is_important if either is True)
                    existing = merged_index[term][doc_id]
                    merged_index[term][doc_id] = {
                        'tf': existing['tf'] + posting_data['tf'],
                        'is_important': existing['is_important'] or posting_data.get('is_important', False)
                    }
        
        # Save merged index
        self._save_final_index_from_dict(merged_index)
    
    def _save_final_index(self):
        """Save final index from in-memory structure"""
        self._save_final_index_from_dict(self.index)
    
    def _save_final_index_from_dict(self, index_dict):
        """Save index dictionary to final index file"""
        final_index_file = os.path.join(self.output_dir, 'inverted_index.json')
        
        # Convert to JSON-serializable format
        index_data = {}
        for term, postings in index_dict.items():
            index_data[term] = {
                str(doc_id): posting_data 
                for doc_id, posting_data in postings.items()
            }
        
        print(f"  Saving final merged index to {final_index_file}...")
        with open(final_index_file, 'w', encoding='utf-8') as f:
            json.dump(index_data, f)
    
    def _save_doc_mappings(self):
        """Save final document mappings"""
        # Collect all doc mappings from partial files
        all_doc_ids = {}
        all_doc_id_to_url = {}
        
        for i in range(self.partial_index_count):
            partial_mapping_file = os.path.join(
                self.partial_index_dir,
                f'partial_mapping_{i:03d}.json'
            )
            
            if os.path.exists(partial_mapping_file):
                with open(partial_mapping_file, 'r', encoding='utf-8') as f:
                    mapping_data = json.load(f)
                    all_doc_ids.update(mapping_data.get('url_to_id', {}))
                    # Convert string keys back to int for id_to_url
                    id_to_url = mapping_data.get('id_to_url', {})
                    for k, v in id_to_url.items():
                        all_doc_id_to_url[int(k)] = v
        
        # Merge with current in-memory mappings
        all_doc_ids.update(self.doc_ids)
        all_doc_id_to_url.update(self.doc_id_to_url)
        
        # Save final mappings
        doc_mapping_file = os.path.join(self.output_dir, 'doc_mapping.json')
        with open(doc_mapping_file, 'w', encoding='utf-8') as f:
            json.dump({
                'url_to_id': all_doc_ids,
                'id_to_url': {str(k): v for k, v in all_doc_id_to_url.items()}
            }, f, indent=2)
    
    def get_num_documents(self):
        """Get the number of indexed documents"""
        return len(self.doc_ids) if self.partial_index_count == 0 else self.next_doc_id
    
    def get_num_unique_tokens(self, output_dir=None):
        """
        Get the number of unique tokens in the final index
        Note: This requires loading the final index file
        """
        if output_dir is None:
            output_dir = self.output_dir
        
        final_index_file = os.path.join(output_dir, 'inverted_index.json')
        if not os.path.exists(final_index_file):
            return len(self.index)
        
        # Count unique tokens from final index file
        with open(final_index_file, 'r', encoding='utf-8') as f:
            index_data = json.load(f)
            return len(index_data)
    
    def get_index_size_kb(self, output_dir=None):
        """
        Get the size of the index on disk in KB
        """
        if output_dir is None:
            output_dir = self.output_dir
        
        total_size = 0
        index_file = os.path.join(output_dir, 'inverted_index.json')
        doc_mapping_file = os.path.join(output_dir, 'doc_mapping.json')
        
        if os.path.exists(index_file):
            total_size += os.path.getsize(index_file)
        if os.path.exists(doc_mapping_file):
            total_size += os.path.getsize(doc_mapping_file)
        
        return total_size / 1024.0  # Convert to KB
    
    def get_partial_index_count(self):
        """Get the number of partial indexes created"""
        return self.partial_index_count

