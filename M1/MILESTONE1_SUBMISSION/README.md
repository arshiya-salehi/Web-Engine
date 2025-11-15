# Milestone 1 Submission - Developer Option

## Submission Contents

This submission contains all files required for Milestone 1 of the Search Engine assignment (Algorithms and Data Structures Developer Option).

All files are in a flat structure (no subdirectories) for easy submission.

## Files Included

### Implementation Files
- **`build_index_disk.py`** - Main disk-based indexer script
- **`disk_indexer.py`** - Disk-based indexer with periodic offloading
- **`generate_reports.py`** - Report generator
- **`html_parser.py`** - HTML parsing module
- **`tokenizer.py`** - Token extraction module
- **`stemmer.py`** - Porter stemming module

### Configuration
- **`requirements.txt`** - Python dependencies
- **`setup.sh`** - Setup script

### Generated Files
- **`milestone1_report_developer.pdf`** - PDF report with analytics table
- **`index_stats.json`** - Statistics data
- **`inverted_index.json`** - Main inverted index (14 MB)
- **`doc_mapping.json`** - URL to document ID mappings

### Documentation
- **`README.md`** - This file

## Setup Instructions

1. Install dependencies:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   source venv/bin/activate
   ```

   Or manually:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   python3 -c "import nltk; nltk.download('punkt')"
   ```

## Running the Code

### Build Index

```bash
python3 build_index_disk.py <path_to_dataset>
```

Example:
```bash
python3 build_index_disk.py ../DEV
```

### Generate Report

```bash
python3 generate_reports.py
```

## Report

The PDF report (`milestone1_report_developer.pdf`) contains:
- Approach specifications
- Index analytics table:
  - Number of indexed documents: 1,212
  - Number of unique tokens: 13,126
  - Total size of index on disk: 14,438.72 KB
- Requirement verification (≥3 offloads during construction)
- Implementation details

## Index Statistics

- **Number of indexed documents:** 1,212
- **Number of unique tokens:** 13,126
- **Total size of index on disk:** 14,438.72 KB (~14 MB)
- **Partial indexes created (offloads):** 4 (requirement: ≥3)

## Requirements Met

✅ **Inverted index structure:** Map with token → postings  
✅ **Posting contains:** Document ID and term frequency (tf)  
✅ **Data source:** Larger collection (DEV dataset)  
✅ **Code submitted:** All implementation files  
✅ **PDF report:** Contains analytics table with all required metrics  
✅ **Disk-based indexing:** Offloads ≥3 times during construction  
✅ **Partial indexes merged:** All partial indexes merged at end  

## Index Structure

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

## Notes

- All files are in a flat structure (no subdirectories)
- The index was built using the ANALYST dataset for testing (1,212 documents)
- For production use with DEV dataset (~56,000 pages), the same code will work
- The disk-based approach ensures memory efficiency for large datasets
- All requirements for Milestone 1 are satisfied
