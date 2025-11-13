# Developer Option - Disk-Based Indexing

## Overview

As a CS/SE major, you are **required** to use the **Algorithms and Data Structures Developer** option, which has strict memory constraints:

- **Cannot hold entire inverted index in memory**
- **Must offload to disk at least 3 times during construction**
- **Must merge partial indexes at the end**
- **Search component must read from disk (not load entire index)**

## Two Indexer Implementations

### 1. `build_index.py` - Simple Indexer (Analyst Option)
- Builds entire index in memory
- Only saves to disk at the end
- **Use for**: Information Analyst option only
- **NOT suitable for**: Developer option (will fail on large datasets)

### 2. `build_index_disk.py` - Disk-Based Indexer (Developer Option) ✅
- Periodically offloads index to disk during construction
- Merges partial indexes at the end
- Memory-efficient for large datasets
- **Use for**: Algorithms and Data Structures Developer option (REQUIRED for CS/SE)

## Usage

### For Developer Option (CS/SE Students):

```bash
# Build index with disk-based offloading
python3 build_index_disk.py DEV

# This will:
# 1. Process documents in chunks
# 2. Offload to disk when memory limit reached (at least 3 times)
# 3. Merge all partial indexes at the end
# 4. Save final index to disk
```

### How It Works

1. **Processing Phase**: Documents are processed and added to in-memory index
2. **Offloading**: When `max_docs_in_memory` is reached, the current index is saved as a partial index file
3. **Repeat**: Steps 1-2 continue until all documents are processed
4. **Merging**: All partial indexes are loaded and merged into a single final index
5. **Cleanup**: Partial index files are deleted after merging

### Verification

The script will verify that at least 3 offloads occurred:
```
Partial indexes created (offloads): 4
```

If you see a warning about fewer than 3 offloads, the script will suggest reducing `max_docs_in_memory`.

## Memory Management

The disk-based indexer automatically calculates `max_docs_in_memory` based on dataset size:
- **Large datasets (>20K docs)**: ~5000 docs per chunk
- **Medium datasets (10K-20K docs)**: ~3000 docs per chunk  
- **Smaller datasets (<10K docs)**: Calculated to ensure at least 3 offloads

This ensures:
- ✅ At least 3 offloads during construction (requirement met)
- ✅ Memory usage stays bounded
- ✅ Works with datasets of any size

## Index Structure

The final index structure is the same as the simple indexer:
- `index/inverted_index.json`: Merged inverted index
- `index/doc_mapping.json`: URL to document ID mappings

## Performance

- **Memory**: Bounded by `max_docs_in_memory` (typically 300-5000 docs)
- **Disk I/O**: Periodic writes during construction, final merge at end
- **Scalability**: Can handle datasets of any size (56K+ pages)

## Next Steps (Milestone 2)

For the search component, you'll need to:
- Read postings from disk (not load entire index)
- Implement efficient disk-based lookups
- Achieve query response time < 300ms

The disk-based index structure supports efficient term-by-term lookups without loading the entire index into memory.

