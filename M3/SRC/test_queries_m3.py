"""
M3 Test Queries Framework
Tests search engine with 20+ queries (half good, half poor performing)
"""

import json
import os
import sys
import time
from search_engine_m3 import M3SearchEngine


# Test queries: 20+ queries designed to test various aspects
# Half should perform well, half should perform poorly initially
TEST_QUERIES = [
    # Good performing queries (specific, clear intent)
    {"query": "cristina lopes", "category": "good", "expected": "faculty profile"},
    {"query": "machine learning", "category": "good", "expected": "ML research"},
    {"query": "ACM", "category": "good", "expected": "ACM related content"},
    {"query": "master of software engineering", "category": "good", "expected": "MSWE program"},
    {"query": "informatics department", "category": "good", "expected": "department info"},
    {"query": "computer science faculty", "category": "good", "expected": "CS faculty"},
    {"query": "graduate programs", "category": "good", "expected": "grad programs"},
    {"query": "undergraduate courses", "category": "good", "expected": "undergrad courses"},
    {"query": "research labs", "category": "good", "expected": "research information"},
    {"query": "admissions requirements", "category": "good", "expected": "admissions info"},
    
    # Poor performing queries (ambiguous, short, or too general)
    {"query": "the", "category": "poor", "expected": "too common word"},
    {"query": "a", "category": "poor", "expected": "single letter"},
    {"query": "and", "category": "poor", "expected": "common word"},
    {"query": "computer", "category": "poor", "expected": "too general"},
    {"query": "student", "category": "poor", "expected": "too general"},
    {"query": "program", "category": "poor", "expected": "ambiguous"},
    {"query": "course", "category": "poor", "expected": "too general"},
    {"query": "research", "category": "poor", "expected": "too general"},
    {"query": "university", "category": "poor", "expected": "too general"},
    {"query": "department", "category": "poor", "expected": "too general"},
    
    # Edge cases and challenging queries
    {"query": "artificial intelligence machine learning", "category": "challenging", "expected": "multi-term"},
    {"query": "software engineering graduate program", "category": "challenging", "expected": "specific program"},
    {"query": "data science research", "category": "challenging", "expected": "research area"},
    {"query": "human computer interaction", "category": "challenging", "expected": "HCI research"},
    {"query": "cybersecurity courses", "category": "challenging", "expected": "specific courses"},
    {"query": "phd program requirements", "category": "challenging", "expected": "phd info"},
    {"query": "faculty publications", "category": "challenging", "expected": "publications"},
    {"query": "internship opportunities", "category": "challenging", "expected": "internships"},
    {"query": "scholarship financial aid", "category": "challenging", "expected": "financial aid"},
    {"query": "alumni network", "category": "challenging", "expected": "alumni info"},
]


def test_search_engine(engine, queries, output_file='m3_test_results.json'):
    """
    Test search engine with all queries and collect results
    
    Args:
        engine: SearchEngine instance
        queries: List of query dictionaries
        output_file: Output JSON file path
    """
    print("=" * 70)
    print("M3 Search Engine Test Suite")
    print("=" * 70)
    print()
    
    results = {
        'test_metadata': {
            'total_queries': len(queries),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
        },
        'queries': {}
    }
    
    good_queries = [q for q in queries if q['category'] == 'good']
    poor_queries = [q for q in queries if q['category'] == 'poor']
    challenging_queries = [q for q in queries if q['category'] == 'challenging']
    
    print(f"Testing {len(good_queries)} good queries, {len(poor_queries)} poor queries, "
          f"{len(challenging_queries)} challenging queries\n")
    
    for i, query_info in enumerate(queries, 1):
        query = query_info['query']
        category = query_info['category']
        expected = query_info.get('expected', '')
        
        print(f"[{i}/{len(queries)}] {category.upper()}: '{query}'")
        print("-" * 70)
        
        start_time = time.time()
        search_results = engine.search(query, top_k=10)
        elapsed_time = (time.time() - start_time) * 1000  # ms
        
        print(f"Found {len(search_results)} results in {elapsed_time:.2f} ms")
        
        if search_results:
            print("Top 5 results:")
            for j, (url, score) in enumerate(search_results[:5], 1):
                print(f"  {j}. [{score:.4f}] {url[:80]}...")
        else:
            print("  No results found")
        
        # Store results
        query_results = {
            'query': query,
            'category': category,
            'expected': expected,
            'num_results': len(search_results),
            'query_time_ms': elapsed_time,
            'results': [
                {
                    'rank': rank,
                    'url': url,
                    'score': score
                }
                for rank, (url, score) in enumerate(search_results[:10], 1)
            ]
        }
        
        results['queries'][query] = query_results
        
        print()
    
    # Summary statistics
    print("=" * 70)
    print("SUMMARY STATISTICS")
    print("=" * 70)
    
    good_times = [r['query_time_ms'] for r in results['queries'].values() 
                  if r['category'] == 'good']
    poor_times = [r['query_time_ms'] for r in results['queries'].values() 
                  if r['category'] == 'poor']
    challenging_times = [r['query_time_ms'] for r in results['queries'].values() 
                         if r['category'] == 'challenging']
    
    if good_times:
        print(f"Good queries - Avg time: {sum(good_times)/len(good_times):.2f} ms, "
              f"Min: {min(good_times):.2f} ms, Max: {max(good_times):.2f} ms")
    
    if poor_times:
        print(f"Poor queries - Avg time: {sum(poor_times)/len(poor_times):.2f} ms, "
              f"Min: {min(poor_times):.2f} ms, Max: {max(poor_times):.2f} ms")
    
    if challenging_times:
        print(f"Challenging queries - Avg time: {sum(challenging_times)/len(challenging_times):.2f} ms, "
              f"Min: {min(challenging_times):.2f} ms, Max: {max(challenging_times):.2f} ms")
    
    all_times = good_times + poor_times + challenging_times
    if all_times:
        print(f"\nOverall - Avg time: {sum(all_times)/len(all_times):.2f} ms, "
              f"Min: {min(all_times):.2f} ms, Max: {max(all_times):.2f} ms")
        print(f"Queries under 300ms: {sum(1 for t in all_times if t < 300)}/{len(all_times)}")
        print(f"Queries under 100ms: {sum(1 for t in all_times if t < 100)}/{len(all_times)}")
    
    # Save results
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, output_file)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2)
    
    print(f"\nResults saved to: {output_path}")
    print("=" * 70)
    
    return results


def main():
    """Main test function"""
    # Determine index directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_dir = os.path.join(script_dir, '..', 'index')
    
    if not os.path.exists(index_dir):
        print(f"Error: Index directory not found: {index_dir}")
        print("Please ensure the index has been built.")
        sys.exit(1)
    
    # Initialize search engine
    print("Initializing M3 search engine...")
    try:
        engine = M3SearchEngine(index_dir)
        print("Search engine ready!\n")
    except Exception as e:
        print(f"Error initializing search engine: {e}")
        sys.exit(1)
    
    # Run tests
    test_search_engine(engine, TEST_QUERIES)


if __name__ == '__main__':
    main()

