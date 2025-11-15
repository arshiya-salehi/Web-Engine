# Information Analyst Option

## Requirements

**Option available to all groups formed only by non-CS and non-SE students.**

### Programming Skills Required
- Intro courses

### Main Challenges
- HTML and JSON parsing
- Read/write structured information from/to files or databases

### Corpus
- A small portion of the ICS web pages (analyst.zip)
- Approximately 2,000 web pages

### Indexer
- You can use a database to store the index, or a simple file – whatever is simpler to you
- If you store it in a file, the index is expected to be sufficiently small, so that it fits in memory all at once

### Search Interface
- The response to search queries should be less than 2 seconds

### Note
This project is a great addition to your résumé!

**Tired:** "Wrote a Python script that finds words in Web pages."

**Wired:** "Wrote a search engine from the ground up that is capable of handling two thousand Web pages."

---

## Implementation

This directory contains the **Information Analyst** option implementation.

### Files

- `build_index.py` - Main indexer script (simple in-memory approach)
- `indexer.py` - In-memory inverted index data structure
- `generate_report.py` - Report generator for this option
- `milestone1_report_analyst.pdf` - Generated report (if available)
- `index_stats_analyst.json` - Statistics (if available)

### Shared Files

The following files are shared with the Developer option and located in `../shared/`:
- `html_parser.py` - HTML parsing
- `tokenizer.py` - Token extraction
- `stemmer.py` - Porter stemming
- `requirements.txt` - Python dependencies
- `setup.sh` - Setup script

---

## Usage

### Setup

```bash
# From project root
cd shared
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

### Build Index

```bash
# From ANALYST_OPTION directory
cd ANALYST_OPTION
python3 build_index.py ../ANALYST
```

### Generate Report

```bash
python3 generate_report.py
```

---

## Index Specifications

- **Tokens**: All alphanumeric sequences
- **Stop words**: Not used (all words indexed)
- **Stemming**: Porter stemming algorithm
- **Important words**: Words in bold, headings (h1-h3), and titles are marked
- **Term frequency**: Calculated for each token in each document

---

## Architecture

This implementation uses a **simple in-memory approach**:
1. Builds entire index in memory using Python dictionaries
2. Processes all documents, accumulating index in memory
3. Saves to disk only at the end as JSON files
4. Suitable for small datasets (~2,000 pages)

The index fits entirely in memory, making it simple and straightforward to implement.

