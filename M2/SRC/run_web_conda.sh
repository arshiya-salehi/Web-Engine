#!/bin/bash
# Run web interface using conda Python

echo "=========================================="
echo "M2 Web Search Interface - Using Conda"
echo "=========================================="
echo ""

cd "$(dirname "$0")"

# Use conda Python explicitly
CONDA_PYTHON="/opt/anaconda3/bin/python3"

if [ ! -f "$CONDA_PYTHON" ]; then
    echo "❌ Conda Python not found at $CONDA_PYTHON"
    echo "Trying to find conda Python..."
    CONDA_PYTHON=$(which python3 | grep anaconda)
    if [ -z "$CONDA_PYTHON" ]; then
        echo "❌ Could not find conda Python"
        echo "Please install Flask in your current Python:"
        echo "  pip3 install --user flask"
        exit 1
    fi
fi

echo "Using Python: $CONDA_PYTHON"
echo ""

# Check if Flask is available
if ! $CONDA_PYTHON -c "import flask" 2>/dev/null; then
    echo "Installing Flask in conda environment..."
    $CONDA_PYTHON -m pip install flask
    echo ""
fi

# Check if index exists
if [ ! -d "../index" ]; then
    echo "❌ Error: Index directory not found!"
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

$CONDA_PYTHON web_search.py

