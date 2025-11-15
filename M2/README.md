# Web Engine - Search Engine Index Construction

A comprehensive inverted index builder for web pages, implementing two approaches for different skill levels as part of Milestone 1 of the Search Engine assignment.

## 📋 Table of Contents

- [Overview](#overview)
- [Two Implementation Options](#two-implementation-options)
- [Project Structure](#project-structure)
- [Quick Start](#quick-start)
- [Requirements](#requirements)
- [Index Specifications](#index-specifications)
- [Implementation Details](#implementation-details)
- [Shared Components](#shared-components)
- [Verification](#verification)

---

## Overview

This project implements an inverted index builder for web pages stored in JSON format. It provides **two separate implementations** designed for different skill levels and requirements:

1. **Information Analyst Option** - Simple in-memory indexing for smaller datasets
2. **Algorithms and Data Structures Developer Option** - Disk-based indexing with memory constraints for large datasets

Both implementations share core processing components (HTML parsing, tokenization, stemming) but use different indexing strategies based on their requirements.

---

## Two Implementation Options

### 1. Information Analyst Option

**Who:** Non-CS/non-SE students  
**Location:** `ANALYST_OPTION/`

**Key Characteristics:**
- Simple in-memory indexing
- Corpus: ~2,000 pages (ANALYST dataset)
- Index fits entirely in memory
- Target search response: < 2 seconds
- Programming level: Introductory courses

**Best For:** Groups with non-CS/non-SE students who need a straightforward implementation.

### 2. Algorithms and Data Structures Developer Option

**Who:** CS/SE students (REQUIRED)  
**Location:** `DEVELOPER_OPTION/`

**Key Characteristics:**
- Disk-based indexing with periodic offloading
- Corpus: ~56,000 pages (DEV dataset)
- Cannot hold entire index in memory
- Must offload to disk ≥3 times during construction
- Partial indexes merged at end
- Target search response: ≤ 300ms
- Programming level: Advanced

**Best For:** CS/SE students who need to handle large datasets under memory constraints.

---

## Project Structure

```
Web-Engine/
├── ANALYST_OPTION/          # Information Analyst implementation
│   ├── README.md           # Detailed requirements & usage
│   ├── build_index.py      # Main indexer (simple in-memory)
│   ├── indexer.py          # In-memory index data structure
│   ├── generate_report.py  # Report generator
│   └── ...
│
├── DEVELOPER_OPTION/        # Developer implementation
│   ├── README.md           # Detailed requirements & usage
│   ├── build_index_disk.py # Main indexer (disk-based)
│   ├── disk_indexer.py     # Disk-based indexer with offloading
│   ├── generate_reports.py # Report generator
│   └── ...
│
├── shared/                 # Shared components (used by both)
│   ├── html_parser.py     # HTML parsing
│   ├── tokenizer.py        # Token extraction
│   ├── stemmer.py         # Porter stemming
│   ├── requirements.txt   # Python dependencies
│   ├── setup.sh          # Setup script
│   └── README.md         # Shared components docs
│
├── ANALYST/               # Dataset: Small corpus (~2,000 pages)
└── DEV/                   # Dataset: Large corpus (~56,000 pages)
```

---

## Quick Start

### Setup (One-Time)

Both implementations share the same dependencies. Set up once:

```bash
cd shared
chmod +x setup.sh
./setup.sh
source venv/bin/activate
```

### For Information Analyst Option

```bash
cd ANALYST_OPTION
python3 build_index.py ../ANALYST
python3 generate_report.py
```

### For Developer Option (CS/SE Required)

```bash
cd DEVELOPER_OPTION
python3 build_index_disk.py ../DEV
python3 generate_reports.py
```

---

## Requirements

### Information Analyst Option

**Full Requirements:**
- **Option available to:** All groups formed only by non-CS and non-SE students
- **Programming skills:** Intro courses
- **Main challenges:** HTML and JSON parsing, read/write structured information
- **Corpus:** Small portion of ICS web pages (analyst.zip) - ~2,000 pages
- **Indexer:** Can use database or simple file. If file, index must fit in memory
- **Search interface:** Response time < 2 seconds

**Implementation:**
- Builds entire index in memory using Python dictionaries
- Processes all documents, accumulating index in memory
- Saves to disk only at the end as JSON files
- Simple and straightforward approach

### Developer Option

**Full Requirements:**
- **Option available to:** All students, but **required for CS and SE students**
- **Programming skills:** Advanced
- **Main challenges:** Design efficient data structures, devise efficient file access, balance memory usage and response time
- **Corpus:** All ICS web pages (developer.zip) - ~56,000 pages
- **Index:** Stored in file system (no databases!)
- **Search interface:** Response time ≤ 300ms (ideally ≤ 100ms)

**Operational Constraints:**
- Cannot hold entire inverted index in memory
- Indexer must offload to disk **at least 3 times** during construction
- Partial indexes must be merged at the end
- Search component must read from disk (not load entire index)
- TAs will verify both offloading and disk-based search

**Implementation:**
- Processes documents in memory-bounded chunks
- Offloads to disk when memory limit reached (≥3 times)
- Merges all partial indexes at end
- Memory usage bounded by chunk size
- Works with datasets of any size

---

## Index Specifications

Both implementations use the same index specifications:

- **Tokens:** All alphanumeric sequences extracted from HTML content
- **Stop words:** Not used (all words are indexed)
- **Stemming:** Porter stemming algorithm (NLTK)
- **Important words:** Words in bold (`<strong>`, `<b>`), headings (`<h1>`, `<h2>`, `<h3>`), and titles (`<title>`) are marked as important
- **Term frequency:** Calculated and stored for each token-document pair
- **URL handling:** Fragment parts (#) are ignored

### Index Structure

The inverted index is stored as:
```json
{
  "token": {
    "doc_id": {
      "tf": <term_frequency>,
      "is_important": <boolean>
    }
  }
}
```

---

## Implementation Details

### Analyst Option Architecture

**Files:**
- `build_index.py` - Main indexer script
- `indexer.py` - In-memory index data structure (`InvertedIndex`)

**How it works:**
1. HTML content parsed using BeautifulSoup
2. Text tokenized into alphanumeric sequences
3. Tokens stemmed using Porter stemmer
4. Term frequencies calculated and stored in memory
5. Final index saved to disk as JSON

**Memory Usage:** Entire index held in memory (~14-22 MB for ~2,000 pages)

### Developer Option Architecture

**Files:**
- `build_index_disk.py` - Main disk-based indexer script
- `disk_indexer.py` - Disk-based indexer with offloading (`DiskBasedIndexer`)

**How it works:**
1. Documents processed in memory-bounded chunks
2. When chunk limit reached, index offloaded to disk as partial index
3. Memory cleared, processing continues
4. Steps 1-3 repeat until all documents processed
5. All partial indexes loaded and merged into final index
6. Final index saved, partial files cleaned up

**Memory Usage:** Bounded by chunk size (typically 300-5,000 documents)

**Verification:** Script automatically ensures ≥3 offloads and reports count

---

## Shared Components

Both implementations share the following components located in `shared/`:

### Core Processing Modules

- **`html_parser.py`** - Parses HTML content, extracts text from important tags
- **`tokenizer.py`** - Extracts alphanumeric sequences (tokens) from text
- **`stemmer.py`** - Applies Porter stemming algorithm to tokens

### Setup Files

- **`requirements.txt`** - Python dependencies (beautifulsoup4, nltk, lxml, reportlab)
- **`setup.sh`** - Automated setup script for virtual environment

### Why Shared?

These components are identical for both approaches:
- Same HTML parsing logic
- Same tokenization rules
- Same stemming algorithm
- Same dependencies

Only the **indexing strategy** differs between the two options.

### Import Pattern

Both implementations import shared files using:
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
from html_parser import HTMLParser
from tokenizer import Tokenizer
from stemmer import Stemmer
```

---

## Verification

### Analyst Option Status

✅ **All M1 requirements met:**
- Simple file-based index (JSON)
- Index fits in memory
- Suitable for ~2,000 pages
- Statistics: ~1,200 documents, ~13,000 unique tokens

### Developer Option Status

✅ **All M1 requirements met:**
- File system index (no databases)
- Cannot hold entire index in memory
- Offloads to disk ≥3 times (verified: typically 4+ offloads)
- Partial indexes merged at end
- Memory usage bounded
- Works with 56,000+ pages

**Verification Output:**
```
Partial indexes created (offloads): 4
```
This confirms the requirement is met (≥3 offloads).

---

## Comparison Summary

| Feature | Analyst Option | Developer Option |
|---------|---------------|------------------|
| **Directory** | `ANALYST_OPTION/` | `DEVELOPER_OPTION/` |
| **Main Script** | `build_index.py` | `build_index_disk.py` |
| **Indexer Class** | `InvertedIndex` | `DiskBasedIndexer` |
| **Memory** | Entire index in memory | Bounded chunks |
| **Offloading** | None | Periodic (≥3 times) |
| **Merging** | N/A | Yes (partial indexes) |
| **Corpus** | ANALYST (~2K pages) | DEV (~56K pages) |
| **Target Response** | < 2 seconds | ≤ 300ms |
| **Scalability** | Limited | Unlimited |

---

## Output Files

### After Building Index

**Analyst Option:**
- `index/inverted_index.json` - Main inverted index
- `index/doc_mapping.json` - URL to document ID mappings
- `index_stats_analyst.json` - Statistics
- `milestone1_report_analyst.pdf` - PDF report

**Developer Option:**
- `index/inverted_index.json` - Merged inverted index
- `index/doc_mapping.json` - URL to document ID mappings
- `index_stats.json` - Statistics (includes partial_indexes count)
- `milestone1_report_developer.pdf` - PDF report

### Report Contents

Both reports include:
- Approach specifications
- Index analytics table (documents, tokens, size)
- Implementation details
- Requirement verification (Developer report shows offload count)

---

## Next Steps (Milestone 2)

### Analyst Option
- Implement search component
- Target: Query response < 2 seconds
- Can load entire index in memory for fast lookups

### Developer Option
- Implement disk-based search component
- Target: Query response ≤ 300ms
- Must read postings from disk (not load entire index)
- Requires efficient disk-based data structures

---

## Notes

- Both implementations are **completely separate** and can be used independently
- They share only the core processing modules (parsing, tokenization, stemming)
- Each has its own indexer implementation and report generator
- The shared components are in `shared/` to avoid duplication
- All duplicate files have been removed from the root directory

---

## Documentation

For more detailed information:
- `ANALYST_OPTION/README.md` - Analyst requirements and detailed usage
- `DEVELOPER_OPTION/README.md` - Developer requirements and detailed usage
- `shared/README.md` - Shared components documentation

---

## License & Credits

This project is part of CS 121 Search Engine assignment. Both implementations meet all Milestone 1 requirements and are ready for submission.
