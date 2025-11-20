#!/bin/bash
# Simple script to run web interface using conda Python

cd "$(dirname "$0")"

echo "Starting web server with conda Python..."
echo ""

# Use conda Python (which has Flask installed)
/opt/anaconda3/bin/python3 web_search.py

