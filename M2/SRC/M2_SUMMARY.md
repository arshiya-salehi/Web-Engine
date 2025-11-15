# Milestone 2 Implementation Summary

## Overview
This document summarizes the implementation of Milestone 2: Retrieval Component for the Search Engine project.

## Files Created/Modified

### New Files
1. **search_engine.py** - Core search engine implementation
   - `SearchEngine` class with boolean AND query processing
   - TF-IDF scoring implementation
   - Important word boosting (1.5x multiplier)
   - Index caching for performance

2. **search.py** - Interactive console search interface
   - User-friendly command-line interface
   - Real-time query processing
   - Query time measurement

3. **test_queries.py** - Automated testing script
   - Tests all 4 required queries
   - Generates JSON results file
   - Displays results in console

4. **generate_m2_report.py** - PDF report generator
   - Creates formatted PDF report
   - Includes top 5 URLs for each query
   - Implementation details section

5. **README_M2.md** - Documentation for M2
6. **M2_SUMMARY.md** - This file

## Implementation Details

### Boolean AND Queries
- All query terms must be present in a document
- Uses set intersection of posting lists from all terms
- Efficient implementation using Python sets

### TF-IDF Scoring
Formula: `tf_idf = (1 + log(tf)) * log(N/df)`
- `tf`: Term frequency in document
- `df`: Document frequency (number of documents containing term)
- `N`: Total number of documents

### Important Words
Words appearing in:
- Bold tags (`<strong>`, `<b>`)
- Headings (`<h1>`, `<h2>`, `<h3>`)
- Title tags (`<title>`)

Receive a 1.5x boost in their TF-IDF score.

### Query Processing Pipeline
1. Tokenize query (extract alphanumeric sequences)
2. Stem tokens using Porter stemmer
3. Retrieve posting lists for each term
4. Compute intersection (AND operation)
5. Calculate TF-IDF scores for matching documents
6. Sort by score (descending)
7. Return top K results

## Required Test Queries

1. **cristina lopes**
2. **machine learning**
3. **ACM**
4. **master of software engineering**

## Usage Instructions

### Setup
```bash
cd DEVELOPER_OPTION
# Ensure dependencies are installed
pip install -r ../shared/requirements.txt
```

### Run Tests
```bash
python3 test_queries.py
```

### Generate Report
```bash
python3 generate_m2_report.py
```

### Interactive Search
```bash
python3 search.py
```

## Performance Notes

- Index is loaded into memory on first query
- Subsequent queries use cached index
- Document mappings are cached
- Query response times measured and reported

**Note:** For M3, the implementation will need to be optimized to:
- Not load entire index into memory
- Use disk-based access for postings
- Meet ≤ 300ms response time requirement

## Deliverables Checklist

- ✅ Search component with boolean AND queries
- ✅ TF-IDF scoring implementation
- ✅ Test script for required queries
- ✅ Top 5 URLs for each test query
- ✅ Console-based search interface
- ✅ PDF report generator
- ✅ Documentation

## Next Steps (M3)

1. Optimize index access (disk-based, not full memory load)
2. Improve query response time to ≤ 300ms
3. Add additional ranking features
4. Optional: Web interface (extra credit)

