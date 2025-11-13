# Milestone 1 Implementation Summary

## Overview

This implementation builds an inverted index from web pages stored in JSON format, following the specifications for Milestone 1 of the Search Engine assignment.

## Files Created

### Core Modules

1. **`html_parser.py`**
   - Parses HTML content using BeautifulSoup (handles broken HTML)
   - Extracts text from normal content and important elements
   - Identifies important text from: `<title>`, `<h1>`, `<h2>`, `<h3>`, `<strong>`, `<b>`
   - Removes script and style elements

2. **`tokenizer.py`**
   - Extracts alphanumeric sequences from text
   - Uses regex pattern `[a-zA-Z0-9]+`
   - Converts all tokens to lowercase

3. **`stemmer.py`**
   - Applies Porter stemming algorithm using NLTK
   - Automatically downloads NLTK data if needed
   - Stems individual tokens or lists of tokens

4. **`indexer.py`**
   - Implements inverted index data structure
   - Tracks term frequency (tf) for each token in each document
   - Marks tokens as important if they appear in important contexts
   - Maps URLs to document IDs
   - Saves index to disk as JSON
   - Calculates index statistics

5. **`build_index.py`**
   - Main script to build the index
   - Processes all JSON files in a directory tree
   - Handles URL fragments (removes # and everything after)
   - Displays progress and statistics
   - Saves statistics to `index_stats.json`

6. **`generate_report.py`**
   - Generates PDF report with analytics table
   - Uses ReportLab library
   - Includes implementation details
   - Creates professional-looking report

### Supporting Files

- **`requirements.txt`**: Python dependencies
- **`setup.sh`**: Setup script for easy installation
- **`README.md`**: Comprehensive documentation
- **`QUICKSTART.md`**: Quick start guide

## Index Specifications Implemented

✅ **Tokens**: All alphanumeric sequences extracted from HTML content  
✅ **Stop words**: Not used (all words are indexed)  
✅ **Stemming**: Porter stemming algorithm applied to all tokens  
✅ **Important words**: Words in bold, headings (h1-h3), and titles are marked  
✅ **Term frequency**: Calculated and stored for each token-document pair  
✅ **URL handling**: Fragment parts (#) are ignored  

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

## Output Files

After running `build_index.py`:
- `index/inverted_index.json`: Main inverted index
- `index/doc_mapping.json`: URL to document ID mappings
- `index_stats.json`: Statistics for report generation

After running `generate_report.py`:
- `milestone1_report.pdf`: PDF report with analytics table

## Analytics Collected

The indexer collects and reports:
1. **Number of indexed documents**: Total unique documents processed
2. **Number of unique tokens**: Total unique stemmed tokens in the index
3. **Total size of index on disk**: Combined size of index files in KB

## Usage Example

```bash
# Setup (one time)
./setup.sh
source venv/bin/activate

# Build index
python3 build_index.py ANALYST

# Generate report
python3 generate_report.py
```

## Design Decisions

1. **HTML Parsing**: Used BeautifulSoup with `html.parser` for robust handling of broken HTML
2. **Tokenization**: Simple regex-based approach for alphanumeric sequences
3. **Stemming**: Porter stemmer from NLTK (industry standard)
4. **Index Storage**: JSON format for easy inspection and debugging
5. **Important Words**: Tracked separately but combined in term frequency for M1
6. **Document IDs**: Used integer IDs instead of URLs for efficiency

## Next Steps (Future Milestones)

- Add IDF calculation for tf-idf scoring (M2)
- Implement ranking algorithm (M2)
- Add query processing (M2)
- Optimize for large datasets with disk-based indexing (if using DEV option)
- Implement search interface (M3)

