# How to Run the M2 Search Engine

## Quick Start Guide

### Prerequisites
- Python 3.6 or higher
- Index files must exist in `M2/index/` directory (from M1)

---

## Step 1: Navigate to the Project Directory

```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC
```

Or if you're already in the M2 directory:
```bash
cd SRC
```

---

## Step 2: Check Dependencies

Make sure you have the required Python packages:

```bash
# Check if packages are installed
python3 -c "import nltk, json, sys; print('✅ Dependencies OK')"
```

If you get an error, install dependencies:
```bash
# Install from the parcer directory
cd ../parcer
pip3 install -r requirements.txt
cd ../SRC
```

---

## Step 3: Verify Index Files Exist

```bash
# Check if index directory exists
ls -lh ../index/
```

You should see:
- `inverted_index.json` (should be ~14MB)
- `doc_mapping.json` (should be ~232KB)

If these files don't exist, you need to build the index first:
```bash
python3 build_index_disk.py ../Data
```

---

## Step 4: Run the Search Engine

### Option A: Interactive Search Interface

Run the interactive console search:

```bash
python3 search.py
```

You'll see:
```
Initializing search engine...
Loaded 1212 document mappings
Loading index into memory...
Index loaded: 13126 unique terms
Search engine ready!

============================================================
Search Engine - Boolean AND Queries
============================================================
Enter queries to search. Type 'quit' or 'exit' to stop.

Query: 
```

Then you can type queries like:
- `cristina lopes`
- `machine learning`
- `ACM`
- `master of software engineering`
- Or any other query

Type `quit` or `exit` to stop.

### Option B: Test Required Queries

Run the test script to test all 4 required queries:

```bash
python3 test_queries.py
```

This will:
- Test all 4 required queries
- Display results in the console
- Save results to `query_results.json`

Example output:
```
Query: cristina lopes
------------------------------------------------------------
Found 5 results (in 155.54 ms)

1. [36.7490] https://www.informatics.uci.edu/explore/faculty-profiles/cristina-lopes/
2. [27.1273] https://www.informatics.uci.edu/2017/01/
...
```

---

## Step 5: Generate the PDF Report

After running the test queries, generate the PDF report:

```bash
python3 generate_m2_report.py
```

This creates `milestone2_report_developer.pdf` with:
- Top 5 URLs for each query
- Query execution times
- Implementation details

---

## Step 6: Generate Screenshot (For Submission)

Generate the screenshot text file:

```bash
python3 generate_screenshot.py
```

This creates `search_interface_screenshot.txt` showing the search interface in action.

You can also take an actual screenshot by:
1. Running `python3 search.py`
2. Executing a query
3. Taking a screenshot of your terminal/console

---

## Complete Workflow Example

Here's a complete workflow from start to finish:

```bash
# 1. Navigate to SRC directory
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC

# 2. Test all required queries
python3 test_queries.py

# 3. Generate PDF report
python3 generate_m2_report.py

# 4. Generate screenshot
python3 generate_screenshot.py

# 5. (Optional) Try interactive search
python3 search.py
```

---

## Troubleshooting

### Error: "Index directory not found"
**Solution**: Make sure you're running from the `SRC` directory and the `index` folder exists in the parent directory.

```bash
# Check current directory
pwd
# Should be: .../M2/SRC

# Check if index exists
ls ../index/
```

### Error: "ModuleNotFoundError: No module named 'nltk'"
**Solution**: Install dependencies

```bash
# From M2 directory
cd parcer
pip3 install -r requirements.txt
# Or
pip3 install nltk beautifulsoup4 lxml reportlab
```

### Error: "Document mapping file not found"
**Solution**: The index needs to be built first

```bash
# Build the index
python3 build_index_disk.py ../Data
```

### Slow First Query
**Normal**: The first query loads the index into memory (~14MB), so it takes longer (100-200ms). Subsequent queries are much faster (< 10ms).

---

## Quick Test Commands

### Test if search engine works:
```bash
cd M2/SRC
python3 -c "
from search_engine import SearchEngine
import os
engine = SearchEngine(os.path.join('..', 'index'))
results = engine.search('cristina lopes', top_k=3)
print(f'✅ Search works! Found {len(results)} results')
"
```

### Test a single query:
```bash
cd M2/SRC
python3 -c "
from search_engine import SearchEngine
import os
engine = SearchEngine(os.path.join('..', 'index'))
results = engine.search('machine learning', top_k=5)
for i, (url, score) in enumerate(results, 1):
    print(f'{i}. [{score:.4f}] {url}')
"
```

---

## File Locations

After running, you'll have these files in `M2/SRC/`:

- `query_results.json` - Results from test queries
- `milestone2_report_developer.pdf` - PDF report
- `search_interface_screenshot.txt` - Screenshot text (if generated)

---

## Example Session

Here's what a typical session looks like:

```bash
$ cd M2/SRC
$ python3 search.py

Initializing search engine...
Loaded 1212 document mappings
Loading index into memory...
Index loaded: 13126 unique terms
Search engine ready!

============================================================
Search Engine - Boolean AND Queries
============================================================
Enter queries to search. Type 'quit' or 'exit' to stop.

Query: cristina lopes

Found 5 results (in 166.54 ms)

1. [36.7490] https://www.informatics.uci.edu/explore/faculty-profiles/cristina-lopes/
2. [27.1273] https://www.informatics.uci.edu/2017/01/
3. [27.1273] https://www.informatics.uci.edu/2017/10/
4. [27.1273] https://www.informatics.uci.edu/2017/08/
5. [23.3190] https://www.informatics.uci.edu/explore/facts-figures/

------------------------------------------------------------

Query: quit
Goodbye!
```

---

## Need Help?

If you encounter any issues:
1. Check that you're in the `M2/SRC` directory
2. Verify index files exist in `M2/index/`
3. Make sure Python dependencies are installed
4. Check the error message for specific guidance

---

**Happy Searching! 🔍**

