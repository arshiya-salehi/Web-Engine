#!/bin/bash
# Setup script for Web Engine Indexer

echo "Setting up Web Engine Indexer..."

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing dependencies..."
pip install -r requirements.txt

# Download NLTK data
echo "Downloading NLTK data..."
python3 -c "import nltk; nltk.download('punkt', quiet=True)"

echo "Setup complete!"
echo ""
echo "To use the indexer:"
echo "1. Activate the virtual environment: source venv/bin/activate"
echo "2. Run the indexer: python3 build_index.py [DATA_DIR]"
echo "3. Generate report: python3 generate_report.py"

