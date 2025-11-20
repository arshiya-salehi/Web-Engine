#!/bin/bash
# Quick script to start the web interface

echo "=========================================="
echo "M2 Web Search Interface"
echo "=========================================="
echo ""

# Check if Flask is installed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Flask not found. Installing..."
    pip3 install --user flask
    echo ""
fi

# Check if index exists
if [ ! -d "../index" ]; then
    echo "❌ Error: Index directory not found!"
    echo "Please build the index first with: python3 build_index_disk.py ../Data"
    exit 1
fi

echo "✅ Starting web server..."
echo ""
echo "The web interface will be available at:"
echo "   http://localhost:5000"
echo ""
echo "Press Ctrl+C to stop the server"
echo "=========================================="
echo ""

python3 web_search.py

