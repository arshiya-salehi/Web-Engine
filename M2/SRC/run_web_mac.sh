#!/bin/bash
# Mac-friendly script to run web interface

echo "=========================================="
echo "M2 Web Search Interface - macOS"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# Try to use existing venv
if [ -d "../venv" ]; then
    echo "✅ Found virtual environment"
    source ../venv/bin/activate
    echo "Activated virtual environment"
else
    echo "⚠️  No virtual environment found"
    echo "Creating one..."
    cd ..
    python3 -m venv venv
    source venv/bin/activate
    cd SRC
fi

# Install Flask if needed
if ! python3 -c "import flask" 2>/dev/null; then
    echo "Installing Flask..."
    pip install flask
    echo ""
fi

# Check if index exists
if [ ! -d "../index" ]; then
    echo "❌ Error: Index directory not found!"
    echo "Please build the index first."
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

