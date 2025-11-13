# Quick Start Guide - Milestone 1

## Step 1: Install Dependencies

Run the setup script:
```bash
./setup.sh
```

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python3 -c "import nltk; nltk.download('punkt')"
```

## Step 2: Build the Index

For ANALYST dataset (smaller, ~2000 pages):
```bash
python3 build_index.py ANALYST
```

For DEV dataset (larger, ~56,000 pages):
```bash
python3 build_index.py DEV
```

This will:
- Process all JSON files in the specified directory
- Extract and tokenize text from HTML content
- Apply Porter stemming
- Build the inverted index
- Save index to `index/` directory
- Display statistics and save to `index_stats.json`

## Step 3: Generate Report

```bash
python3 generate_report.py
```

This creates `milestone1_report.pdf` with the analytics table.

## Expected Output

After running `build_index.py`, you should see:
```
Building index from ANALYST...
Found X JSON files to process
Processing file 100/X...
...
Processed X documents

Saving index to disk...

==================================================
INDEX STATISTICS
==================================================
Number of indexed documents: X
Number of unique tokens: X
Total size of index on disk: X.XX KB
==================================================
```

## Troubleshooting

**Import errors**: Make sure you've activated the virtual environment:
```bash
source venv/bin/activate
```

**NLTK data error**: Run:
```bash
python3 -c "import nltk; nltk.download('punkt')"
```

**Permission denied on setup.sh**: Run:
```bash
chmod +x setup.sh
```

