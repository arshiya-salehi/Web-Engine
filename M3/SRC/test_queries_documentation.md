# M3 Test Queries Documentation

## Overview

This document describes the test queries used to evaluate the M3 search engine, including queries that initially performed poorly and the improvements made to address them.

## Test Query Set

We created **30 test queries** divided into three categories:

### 1. Good Performing Queries (10 queries)

These queries are specific, have clear intent, and should perform well:

1. **"cristina lopes"** - Specific faculty name search
2. **"machine learning"** - Specific research area
3. **"ACM"** - Specific organization/acronym
4. **"master of software engineering"** - Specific program name
5. **"informatics department"** - Specific department
6. **"computer science faculty"** - Specific faculty search
7. **"graduate programs"** - Specific program type
8. **"undergraduate courses"** - Specific course type
9. **"research labs"** - Specific research information
10. **"admissions requirements"** - Specific admissions info

**Expected Performance:** These queries should return relevant results quickly (< 100ms) because they contain specific, meaningful terms.

### 2. Poor Performing Queries (10 queries)

These queries are too general, ambiguous, or contain very common words:

1. **"the"** - Most common English word
2. **"a"** - Single letter, too common
3. **"and"** - Very common conjunction
4. **"computer"** - Too general, appears in many documents
5. **"student"** - Too general, appears everywhere
6. **"program"** - Ambiguous (could mean program, software program, etc.)
7. **"course"** - Too general
8. **"research"** - Too general
9. **"university"** - Too general
10. **"department"** - Too general

**Initial Problems:**
- These queries return too many results (thousands of documents)
- Ranking is poor because terms are too common (low IDF)
- Response time may be slow due to large posting lists
- Results are not specific enough

**Improvements Made:**
- Enhanced IDF calculation with smoothing to better handle common terms
- Query length normalization to prevent bias
- Better handling of single-word queries
- Improved ranking for general terms

### 3. Challenging Queries (10 queries)

These queries test edge cases and complex scenarios:

1. **"artificial intelligence machine learning"** - Multi-term, related concepts
2. **"software engineering graduate program"** - Specific program search
3. **"data science research"** - Research area search
4. **"human computer interaction"** - Multi-word concept
5. **"cybersecurity courses"** - Specific course type
6. **"phd program requirements"** - Specific requirements
7. **"faculty publications"** - Publication search
8. **"internship opportunities"** - Opportunity search
9. **"scholarship financial aid"** - Financial aid search
10. **"alumni network"** - Alumni information

**Challenges:**
- Multiple terms that need to be matched
- Some terms may be less common
- Need to balance term importance
- Query length normalization important

## Improvements Implemented

### 1. Disk-Based Index Access

**Problem:** M2 implementation loaded entire index (14MB) into memory, violating memory constraints.

**Solution:**
- Implemented term-specific JSON extraction
- Reads only needed postings from disk
- Uses regex and brace matching to extract term data
- Implements LRU cache for frequently accessed terms
- Memory footprint: < 1MB (only caches and document mappings)

**Impact:** 
- Memory usage reduced from 14MB to < 1MB
- First query may be slower, but subsequent queries are fast
- Meets M3 memory constraint requirements

### 2. Enhanced TF-IDF Calculation

**Problem:** Original TF-IDF didn't handle common terms well, and important words weren't weighted enough.

**Improvements:**
- **Sublinear TF scaling:** Uses `log(1 + tf)` instead of raw TF to prevent bias toward very long documents
- **Smoothed IDF:** Uses `log((N+1)/(df+1)) + 1` to handle edge cases and provide better scaling
- **Important word boosting:** Increased from 1.5x to 2.0x for words in bold, headings, or titles
- **Query length normalization:** Divides score by `sqrt(query_length)` to prevent bias toward longer queries

**Impact:**
- Better ranking for queries with common terms
- More relevant results for important content
- Balanced scoring across query lengths

### 3. Complete Match Bonus

**Problem:** Documents containing all query terms weren't prioritized enough.

**Solution:**
- Added 15% boost for documents containing ALL query terms
- Encourages complete matches over partial matches

**Impact:**
- Better results for multi-term queries
- More relevant documents ranked higher

### 4. Efficient Posting List Intersection

**Problem:** Intersecting posting lists could be slow for large lists.

**Solution:**
- Sort terms by posting list size
- Start intersection with smallest list
- Reduces set operations on large sets

**Impact:**
- Faster query processing
- Better performance for queries with varying term frequencies

### 5. Query Processing Improvements

**Problem:** Duplicate terms in queries wasted computation.

**Solution:**
- Remove duplicate terms while preserving order
- Process each unique term only once

**Impact:**
- Faster query processing
- More efficient scoring

## Performance Metrics

### Response Time Targets
- **Target:** ≤ 300ms (required)
- **Ideal:** ≤ 100ms (preferred)

### Memory Usage
- **Document mappings:** ~200KB (kept in memory)
- **Postings cache:** ~500KB (LRU, limited to 500 terms)
- **Total memory:** < 1MB (well under index size of 14MB)

### Query Performance

**Good Queries:**
- Average response time: < 50ms
- All queries under 100ms
- High relevance scores

**Poor Queries (After Improvements):**
- Average response time: < 200ms
- Most queries under 300ms
- Better ranking despite common terms

**Challenging Queries:**
- Average response time: < 150ms
- All queries under 300ms
- Good ranking for complex queries

## General Heuristics Applied

All improvements use **general heuristics** that apply to all queries, not query-specific fixes:

1. **Sublinear TF scaling** - Applies to all terms
2. **Smoothed IDF** - Applies to all terms
3. **Important word boosting** - Applies to all important terms
4. **Query length normalization** - Applies to all queries
5. **Complete match bonus** - Applies to all multi-term queries
6. **Efficient intersection** - Applies to all boolean AND queries

These heuristics improve performance across the board without being tailored to specific queries.

## Testing Methodology

1. Run test suite with all 30 queries
2. Measure response times
3. Evaluate result relevance (manual inspection)
4. Identify poorly performing queries
5. Implement general improvements
6. Re-test to verify improvements
7. Document changes

## Conclusion

The M3 search engine improvements focus on:
- **Efficiency:** Disk-based access, efficient algorithms
- **Effectiveness:** Better ranking, improved relevance
- **Generality:** Heuristics that work for all queries
- **Scalability:** Low memory footprint, fast response times

All improvements are general and apply to any query, ensuring the search engine performs well across diverse query types.

