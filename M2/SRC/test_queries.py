"""
Test Queries Script
Tests the search engine with required queries and generates results
"""

import sys
import os
import json
import time
from search_engine import SearchEngine


def test_queries():
    """Test search engine with required queries"""
    # Determine index directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_dir = os.path.join(script_dir, '..', 'index')
    
    if not os.path.exists(index_dir):
        print(f"Error: Index directory not found: {index_dir}")
        print("Please run build_index_disk.py first to create the index.")
        sys.exit(1)
    
    # Initialize search engine
    print("Initializing search engine...")
    try:
        engine = SearchEngine(index_dir)
        print("Search engine ready!\n")
    except Exception as e:
        print(f"Error initializing search engine: {e}")
        sys.exit(1)
    
    # Required test queries
    queries = [
        "cristina lopes",
        "machine learning",
        "ACM",
        "master of software engineering"
    ]
    
    print("=" * 60)
    print("Testing Search Engine with Required Queries")
    print("=" * 60)
    print()
    
    all_results = {}
    
    for query in queries:
        print(f"Query: {query}")
        print("-" * 60)
        
        start_time = time.time()
        results = engine.search(query, top_k=5)
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        print(f"Found {len(results)} results (in {elapsed_time:.2f} ms)\n")
        
        query_results = []
        for i, (url, score) in enumerate(results, 1):
            print(f"{i}. [{score:.4f}] {url}")
            query_results.append({
                'rank': i,
                'url': url,
                'score': score
            })
        
        all_results[query] = {
            'results': query_results,
            'num_results': len(results),
            'query_time_ms': elapsed_time
        }
        
        print()
    
    # Save results to JSON file
    results_file = os.path.join(script_dir, 'query_results.json')
    with open(results_file, 'w', encoding='utf-8') as f:
        json.dump(all_results, f, indent=2)
    
    print("=" * 60)
    print(f"Results saved to: {results_file}")
    print("=" * 60)
    
    return all_results


if __name__ == '__main__':
    test_queries()

