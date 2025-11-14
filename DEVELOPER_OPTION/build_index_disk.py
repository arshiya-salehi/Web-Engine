"""
Disk-Based Indexer Script
Builds inverted index with periodic disk offloading (Developer option)
"""

import json
import os
import sys
from pathlib import Path

# Add shared directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from html_parser import HTMLParser
from tokenizer import Tokenizer
from stemmer import Stemmer

# Import local disk indexer
sys.path.insert(0, os.path.dirname(__file__))
from disk_indexer import DiskBasedIndexer


def process_json_file(file_path, html_parser, tokenizer, stemmer):
    """
    Process a single JSON file and extract tokens
    
    Args:
        file_path: Path to JSON file
        html_parser: HTMLParser instance
        tokenizer: Tokenizer instance
        stemmer: Stemmer instance
        
    Returns:
        tuple: (url, normal_tokens, important_tokens) or None if error
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        url = data.get('url', '')
        content = data.get('content', '')
        
        if not url or not content:
            return None
        
        # Remove fragment part from URL (ignore # and everything after)
        if '#' in url:
            url = url.split('#')[0]
        
        # Parse HTML
        parsed = html_parser.parse(content)
        
        # Tokenize
        normal_tokens = tokenizer.tokenize(parsed['normal_text'])
        important_tokens = tokenizer.tokenize(parsed['important_text'])
        
        # Stem tokens
        normal_tokens = stemmer.stem_tokens(normal_tokens)
        important_tokens = stemmer.stem_tokens(important_tokens)
        
        return url, normal_tokens, important_tokens
    
    except Exception as e:
        print(f"Error processing {file_path}: {e}", file=sys.stderr)
        return None


def build_index_disk(data_dir, output_dir='index', max_docs_in_memory=10000):
    """
    Build inverted index with disk-based offloading
    
    Args:
        data_dir: Directory containing subdirectories with JSON files
        output_dir: Directory to save the index
        max_docs_in_memory: Maximum documents to process before offloading
    """
    print(f"Building disk-based index from {data_dir}...")
    print(f"Memory limit: {max_docs_in_memory} documents per partial index")
    print("="*60)
    
    # Initialize components
    html_parser = HTMLParser()
    tokenizer = Tokenizer()
    stemmer = Stemmer()
    
    # Use disk-based indexer
    index = DiskBasedIndexer(output_dir, max_docs_in_memory)
    
    # Find all JSON files
    json_files = list(Path(data_dir).rglob('*.json'))
    total_files = len(json_files)
    
    print(f"Found {total_files} JSON files to process\n")
    
    # Process each file
    processed_count = 0
    for i, json_file in enumerate(json_files, 1):
        if i % 100 == 0:
            print(f"Processing file {i}/{total_files}... "
                  f"(Partial indexes created: {index.get_partial_index_count()})")
        
        result = process_json_file(json_file, html_parser, tokenizer, stemmer)
        if result:
            url, normal_tokens, important_tokens = result
            index.add_document(url, normal_tokens, important_tokens)
            processed_count += 1
    
    print(f"\nProcessed {processed_count} documents")
    print(f"Created {index.get_partial_index_count()} partial indexes during construction")
    
    # Finalize: merge all partial indexes
    print("\nFinalizing index...")
    index.finalize()
    
    # Calculate statistics
    num_docs = index.get_num_documents()
    num_tokens = index.get_num_unique_tokens(output_dir)
    index_size_kb = index.get_index_size_kb(output_dir)
    partial_count = index.get_partial_index_count()
    
    print("\n" + "="*60)
    print("INDEX STATISTICS")
    print("="*60)
    print(f"Number of indexed documents: {num_docs}")
    print(f"Number of unique tokens: {num_tokens}")
    print(f"Total size of index on disk: {index_size_kb:.2f} KB")
    print(f"Partial indexes created (offloads): {partial_count}")
    print("="*60)
    
    # Verify we offloaded at least 3 times
    if partial_count < 3:
        print(f"\n⚠️  WARNING: Only {partial_count} partial indexes created.")
        print("   Requirements specify at least 3 offloads during construction.")
        print("   Consider reducing max_docs_in_memory to ensure more offloads.")
    
    return {
        'num_documents': num_docs,
        'num_unique_tokens': num_tokens,
        'index_size_kb': index_size_kb,
        'partial_indexes': partial_count
    }


if __name__ == '__main__':
    # Determine which dataset to use
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    else:
        # Default to DEV dataset for Developer option
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, 'DEV')
        if not os.path.exists(data_dir):
            data_dir = os.path.join(script_dir, 'ANALYST')
    
    if not os.path.exists(data_dir):
        print(f"Error: Data directory '{data_dir}' does not exist")
        sys.exit(1)
    
    # Determine max_docs_in_memory based on dataset size
    json_files = list(Path(data_dir).rglob('*.json'))
    total_files = len(json_files)
    
    # Calculate to ensure at least 3 offloads (4 partial indexes total)
    # We want: total_files / max_docs >= 3, so max_docs <= total_files / 3
    # But also want reasonable chunk sizes, so use total_files / 4 for safety
    if total_files > 20000:
        max_docs = max(5000, total_files // 10)  # Ensure at least 10 offloads for large datasets
    elif total_files > 10000:
        max_docs = max(3000, total_files // 8)  # Ensure at least 8 offloads
    elif total_files > 5000:
        max_docs = max(1500, total_files // 4)  # Ensure at least 4 offloads
    else:
        # For smaller datasets, ensure at least 3 offloads
        max_docs = max(300, total_files // 4)  # Will create at least 3-4 partial indexes
    
    print(f"Estimated documents: ~{total_files}")
    print(f"Using max_docs_in_memory: {max_docs} (will ensure at least 3 offloads)\n")
    
    # Build the index
    stats = build_index_disk(data_dir, max_docs_in_memory=max_docs)
    
    # Save statistics to file for report generation
    stats_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index_stats.json')
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\nStatistics saved to {stats_file}")

