"""
Generate Screenshot Text Output
Creates a text file showing the search interface in action
This can be used as a "screenshot" for the M2 report
"""

import sys
import os
import time
from search_engine import SearchEngine


def generate_screenshot_output():
    """Generate text output showing search interface in action"""
    
    # Determine index directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    index_dir = os.path.join(script_dir, '..', 'index')
    
    if not os.path.exists(index_dir):
        print(f"Error: Index directory not found: {index_dir}")
        sys.exit(1)
    
    # Initialize search engine
    output_lines = []
    output_lines.append("=" * 70)
    output_lines.append("Search Engine - Boolean AND Queries")
    output_lines.append("=" * 70)
    output_lines.append("")
    
    try:
        engine = SearchEngine(index_dir)
        output_lines.append("Search engine initialized successfully.")
        output_lines.append("")
    except Exception as e:
        output_lines.append(f"Error: {e}")
        return output_lines
    
    # Test queries (required M2 queries)
    test_queries = [
        "cristina lopes",
        "machine learning",
        "ACM",
        "master of software engineering"
    ]
    
    for query in test_queries:
        output_lines.append("-" * 70)
        output_lines.append(f"Query: {query}")
        output_lines.append("-" * 70)
        output_lines.append("")
        
        # Perform search
        start_time = time.time()
        results = engine.search(query, top_k=5)
        elapsed_time = (time.time() - start_time) * 1000
        
        # Display results
        output_lines.append(f"Found {len(results)} results (in {elapsed_time:.2f} ms)")
        output_lines.append("")
        
        if results:
            for i, (url, score) in enumerate(results, 1):
                output_lines.append(f"{i}. [{score:.4f}] {url}")
        else:
            output_lines.append("No results found.")
        
        output_lines.append("")
    
    output_lines.append("=" * 70)
    output_lines.append("End of search interface demonstration")
    output_lines.append("=" * 70)
    
    return output_lines


def main():
    """Main function"""
    output_lines = generate_screenshot_output()
    
    # Print to console
    for line in output_lines:
        print(line)
    
    # Save to file
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(script_dir, 'search_interface_screenshot.txt')
    
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(output_lines))
    
    print(f"\nScreenshot text saved to: {output_file}")
    print("You can include this in your report or take a screenshot of the console output.")


if __name__ == '__main__':
    main()

