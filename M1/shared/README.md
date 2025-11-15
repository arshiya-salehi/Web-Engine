# Shared Components

This directory contains files that are **shared between both implementations** (Analyst and Developer options).

## Shared Files

### Core Processing Modules

- **`html_parser.py`** - Parses HTML content and extracts text from important tags (bold, headings, titles)
- **`tokenizer.py`** - Extracts alphanumeric sequences (tokens) from text
- **`stemmer.py`** - Applies Porter stemming algorithm to tokens

### Setup Files

- **`requirements.txt`** - Python dependencies (beautifulsoup4, nltk, lxml, reportlab)
- **`setup.sh`** - Automated setup script for virtual environment

## Usage

Both `ANALYST_OPTION` and `DEVELOPER_OPTION` directories import these shared modules.

The implementations add these to the Python path:
```python
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'shared'))
```

## Setup

To set up the shared dependencies:

```bash
cd shared
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

## Why Shared?

These components are identical for both approaches:
- HTML parsing logic is the same
- Tokenization rules are the same
- Stemming algorithm is the same
- Dependencies are the same

Only the **indexing strategy** differs:
- **Analyst**: Simple in-memory indexing
- **Developer**: Disk-based indexing with offloading

