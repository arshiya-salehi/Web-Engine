# Algorithms and Data Structures Developer Option

## Requirements

**Option available to all students, but required for CS and SE students.**

### Programming Skills Required
- Advanced

### Main Challenges
- Design efficient data structures
- Devise efficient file access
- Balance memory usage and response time

### Corpus
- All ICS web pages (developer.zip)
- Approximately 56,000 web pages

### Index
- Your index should be stored in one or more files in the file system (no databases!)

### Search Interface
- The response to search queries should be ≤ 300ms
- Ideally, it would be ≤ 100ms, or less
- You won't be penalized if it's higher (as long as it's kept ≤ 300ms)

### Operational Constraints

Typically, the cloud servers/containers that run search engines don't have a lot of memory, but they need to handle large amounts of data. As such, you must design and implement your programs as if you are dealing with very large amounts of data, so large that you cannot hold the inverted index all in memory.

**Your indexer must:**
- Offload the inverted index hash map from main memory to a partial index on disk **at least 3 times** during index construction
- Merge those partial indexes in the end
- Optionally, after or during merging, they can also be split into separate index files with term ranges

**Your search component must:**
- Not load the entire inverted index in main memory
- Instead, it must read the postings from the index(es) files on disk

**The TAs will check that both of these things are happening.**

### Note
This project is a great addition to your résumé!

**Tired:** "Wrote a Web search engine using ElasticSearch."

**Wired:** "Wrote a Web search engine from the ground up that is capable of handling tens of thousands of Web pages, under harsh operational constraints and having a query response time under 300ms."

---

## Implementation

This directory contains the **Algorithms and Data Structures Developer** option implementation.

### Files

- `build_index_disk.py` - Main disk-based indexer script
- `disk_indexer.py` - Disk-based indexer with periodic offloading
- `generate_reports.py` - Report generator for this option
- `milestone1_report_developer.pdf` - Generated report (if available)
- `index_stats.json` - Statistics including partial index count (if available)

### Shared Files

The following files are shared with the Analyst option and located in `../shared/`:
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
# From DEVELOPER_OPTION directory
cd DEVELOPER_OPTION
python3 build_index_disk.py ../DEV
```

The script will automatically:
- Calculate chunk size to ensure at least 3 offloads
- Process documents in memory-bounded chunks
- Offload to disk when memory limit reached
- Merge all partial indexes at the end
- Verify that ≥3 offloads occurred

### Generate Report

```bash
python3 generate_reports.py
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

This implementation uses a **disk-based approach with periodic offloading**:

1. **Processing Phase**: Documents processed and added to in-memory index chunk
2. **Offloading**: When memory limit reached, current index saved as partial index file
3. **Repeat**: Steps 1-2 continue until all documents processed
4. **Merging**: All partial indexes loaded and merged into single final index
5. **Cleanup**: Partial index files deleted after merging

### Memory Management

- Memory usage bounded by chunk size (typically 300-5,000 documents)
- Automatically calculates chunk size to ensure ≥3 offloads
- Works with datasets of any size (56,000+ pages)

### Verification

The script verifies and reports:
- Number of partial indexes created (must be ≥3)
- Warning if requirement not met

---

## Requirements Verification

When you run the indexer, you'll see output like:
```
Partial indexes created (offloads): 4
```

This confirms the requirement is met (≥3 offloads).

