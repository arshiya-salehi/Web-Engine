"""
Main Indexer Script
Builds inverted index from JSON files containing web pages
"""

import json
import os
import sys
from pathlib import Path
from html_parser import HTMLParser
from tokenizer import Tokenizer
from stemmer import Stemmer
from indexer import InvertedIndex


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


def build_index(data_dir, output_dir='index'):
    """
    Build inverted index from JSON files in data directory
    
    Args:
        data_dir: Directory containing subdirectories with JSON files
        output_dir: Directory to save the index
    """
    print(f"Building index from {data_dir}...")
    
    # Initialize components
    html_parser = HTMLParser()
    tokenizer = Tokenizer()
    stemmer = Stemmer()
    index = InvertedIndex()
    
    # Find all JSON files
    json_files = list(Path(data_dir).rglob('*.json'))
    total_files = len(json_files)
    
    print(f"Found {total_files} JSON files to process")
    
    # Process each file
    processed_count = 0
    for i, json_file in enumerate(json_files, 1):
        if i % 100 == 0:
            print(f"Processing file {i}/{total_files}...")
        
        result = process_json_file(json_file, html_parser, tokenizer, stemmer)
        if result:
            url, normal_tokens, important_tokens = result
            index.add_document(url, normal_tokens, important_tokens)
            processed_count += 1
    
    print(f"\nProcessed {processed_count} documents")
    
    # Save index to disk
    print("Saving index to disk...")
    index.save_to_disk(output_dir)
    
    # Calculate statistics
    num_docs = index.get_num_documents()
    num_tokens = index.get_num_unique_tokens()
    index_size_kb = index.get_index_size_kb(output_dir)
    
    print("\n" + "="*50)
    print("INDEX STATISTICS")
    print("="*50)
    print(f"Number of indexed documents: {num_docs}")
    print(f"Number of unique tokens: {num_tokens}")
    print(f"Total size of index on disk: {index_size_kb:.2f} KB")
    print("="*50)
    
    return {
        'num_documents': num_docs,
        'num_unique_tokens': num_tokens,
        'index_size_kb': index_size_kb
    }


if __name__ == '__main__':
    # Determine which dataset to use
    if len(sys.argv) > 1:
        data_dir = sys.argv[1]
    else:
        # Default to ANALYST dataset
        script_dir = os.path.dirname(os.path.abspath(__file__))
        data_dir = os.path.join(script_dir, 'ANALYST')
        if not os.path.exists(data_dir):
            data_dir = os.path.join(script_dir, 'DEV')
    
    if not os.path.exists(data_dir):
        print(f"Error: Data directory '{data_dir}' does not exist")
        sys.exit(1)
    
    # Build the index
    stats = build_index(data_dir)
    
    # Save statistics to file for report generation
    stats_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'index_stats.json')
    with open(stats_file, 'w') as f:
        json.dump(stats, f, indent=2)
    
    print(f"\nStatistics saved to {stats_file}")

