"""
Web-based Search Interface for M2
Flask web application for the search engine
Extra Credit: Web interface (2 points)
"""

import os
import sys
import time
from flask import Flask, render_template, request, jsonify
from search_engine import SearchEngine

app = Flask(__name__)

# Initialize search engine
script_dir = os.path.dirname(os.path.abspath(__file__))
index_dir = os.path.join(script_dir, '..', 'index')

# Check if index exists
if not os.path.exists(index_dir):
    print(f"Error: Index directory not found: {index_dir}")
    print("Please ensure the index has been built.")
    sys.exit(1)

print("Initializing search engine...")
try:
    search_engine = SearchEngine(index_dir)
    print("Search engine ready!")
except Exception as e:
    print(f"Error initializing search engine: {e}")
    sys.exit(1)


@app.route('/')
def index():
    """Main search page"""
    return render_template('search.html')


@app.route('/search', methods=['POST'])
def search():
    """Handle search requests"""
    try:
        data = request.get_json()
        query = data.get('query', '').strip()
        
        if not query:
            return jsonify({
                'success': False,
                'error': 'Please enter a query'
            })
        
        # Perform search
        start_time = time.time()
        results = search_engine.search(query, top_k=10)
        elapsed_time = (time.time() - start_time) * 1000  # Convert to milliseconds
        
        # Format results
        formatted_results = []
        for i, (url, score) in enumerate(results, 1):
            formatted_results.append({
                'rank': i,
                'url': url,
                'score': round(score, 4)
            })
        
        return jsonify({
            'success': True,
            'query': query,
            'num_results': len(results),
            'query_time_ms': round(elapsed_time, 2),
            'results': formatted_results
        })
    
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e)
        })


@app.route('/test_queries')
def test_queries():
    """Test page with required queries"""
    return render_template('test_queries.html')


if __name__ == '__main__':
    print("\n" + "=" * 60)
    print("Web Search Interface")
    print("=" * 60)
    print("Starting web server...")
    print("Open your browser and go to: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    print("=" * 60 + "\n")
    
    try:
        app.run(debug=True, host='0.0.0.0', port=5000)
    except OSError as e:
        if "Address already in use" in str(e):
            print("\n⚠️  Port 5000 is already in use. Trying port 5001...")
            app.run(debug=True, host='0.0.0.0', port=5001)
            print("Open your browser and go to: http://localhost:5001")
        else:
            raise

