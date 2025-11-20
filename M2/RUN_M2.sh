#!/bin/bash
# Quick script to run M2 search engine

echo "=========================================="
echo "M2 Search Engine - Quick Start"
echo "=========================================="
echo ""

# Navigate to SRC directory
cd "$(dirname "$0")/SRC"

# Check if index exists
if [ ! -d "../index" ]; then
    echo "❌ Error: Index directory not found!"
    echo "Please build the index first with: python3 build_index_disk.py ../Data"
    exit 1
fi

echo "✅ Index directory found"
echo ""
echo "Choose an option:"
echo "1. Run interactive search"
echo "2. Test all required queries"
echo "3. Generate PDF report"
echo "4. Generate screenshot"
echo "5. Do everything (test + report + screenshot)"
echo ""
read -p "Enter choice (1-5): " choice

case $choice in
    1)
        echo "Starting interactive search..."
        python3 search.py
        ;;
    2)
        echo "Testing all required queries..."
        python3 test_queries.py
        ;;
    3)
        echo "Generating PDF report..."
        python3 generate_m2_report.py
        ;;
    4)
        echo "Generating screenshot..."
        python3 generate_screenshot.py
        ;;
    5)
        echo "Running complete workflow..."
        echo ""
        echo "Step 1: Testing queries..."
        python3 test_queries.py
        echo ""
        echo "Step 2: Generating report..."
        python3 generate_m2_report.py
        echo ""
        echo "Step 3: Generating screenshot..."
        python3 generate_screenshot.py
        echo ""
        echo "✅ Complete! Check the generated files."
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
