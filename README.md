# Web Engine - Milestone 1: Index Construction

This project implements an inverted index builder for web pages as part of Milestone 1 of the Search Engine assignment.

## Project Structure

- `html_parser.py`: Parses HTML content and extracts text from important tags (bold, headings, titles)
- `tokenizer.py`: Extracts alphanumeric sequences (tokens) from text
- `stemmer.py`: Applies Porter stemming to tokens
- `indexer.py`: Builds and manages the inverted index data structure
- `build_index.py`: Main script to build the index from JSON files
- `generate_report.py`: Generates PDF report with index analytics
- `requirements.txt`: Python dependencies

## Setup

### Option 1: Using Virtual Environment (Recommended)

```bash
# Make setup script executable
chmod +x setup.sh

# Run setup script
./setup.sh

# Activate virtual environment
source venv/bin/activate
```

### Option 2: Manual Setup

```bash
# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Download NLTK data
python3 -c "import nltk; nltk.download('punkt')"
```

## Usage

### Important: Choose the Right Indexer

**For CS/SE Majors (Developer Option - REQUIRED):**
```bash
python3 build_index_disk.py DEV
```

**For Non-CS/SE Majors (Analyst Option):**
```bash
python3 build_index.py ANALYST
```

### Building the Index

**Developer Option (Disk-Based - CS/SE Required):**
```bash
# Uses disk-based indexing with periodic offloading
python3 build_index_disk.py DEV
```

**Analyst Option (Simple - Non-CS/SE):**
```bash
# Builds entire index in memory, then saves
python3 build_index.py ANALYST
```

See `DEVELOPER_README.md` for details on the Developer option requirements.

The index will be saved in the `index/` directory:
- `inverted_index.json`: Main inverted index
- `doc_mapping.json`: URL to document ID mappings

### Generating the Report

After building the index, generate the PDF report:
```bash
python3 generate_report.py
```

This will create `milestone1_report.pdf` with the analytics table.

## Index Specifications

- **Tokens**: All alphanumeric sequences in the dataset
- **Stop words**: Not used (all words are indexed)
- **Stemming**: Porter stemming algorithm
- **Important words**: Words in bold (`<strong>`, `<b>`), headings (`<h1>`, `<h2>`, `<h3>`), and titles (`<title>`) are marked as important
- **Term frequency**: Calculated for each token in each document

## Index Structure

The inverted index is stored as:
```
{
  "token": {
    "doc_id": {
      "tf": term_frequency,
      "is_important": boolean
    }
  }
}
```

## Output

The indexer outputs:
- Number of indexed documents
- Number of unique tokens
- Total size of index on disk (in KB)

These statistics are also saved to `index_stats.json` and included in the PDF report.
