"""
Search Interface
Console-based search interface for the search engine
"""

import sys
import os
import time
from search_engine import SearchEngine


def main():
    """Main search interface"""
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
    
    # Interactive search loop
    print("=" * 60)
    print("Search Engine - Boolean AND Queries")
    print("=" * 60)
    print("Enter queries to search. Type 'quit' or 'exit' to stop.\n")
    
    while True:
        try:
            query = input("Query: ").strip()
            
            if not query:
                continue
            
            if query.lower() in ['quit', 'exit', 'q']:
                print("Goodbye!")
                break
            
            # Perform search
            start_time = time.time()
            results = engine.search(query, top_k=10)
            elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
            
            # Display results
            print(f"\nFound {len(results)} results (in {elapsed_time:.2f} ms)\n")
            
            if results:
                for i, (url, score) in enumerate(results, 1):
                    print(f"{i}. [{score:.4f}] {url}")
            else:
                print("No results found.")
            
            print("\n" + "-" * 60 + "\n")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye!")
            break
        except Exception as e:
            print(f"Error: {e}", file=sys.stderr)


if __name__ == '__main__':
    main()

