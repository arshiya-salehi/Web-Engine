# Installing Flask on macOS

## Quick Installation

Since you're on macOS, use the `--user` flag to install Flask:

```bash
pip3 install --user flask
```

## Alternative Methods

### Method 1: Using --user flag (Recommended)
```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC
pip3 install --user flask
```

### Method 2: Using virtual environment (Best Practice)
```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2
python3 -m venv venv
source venv/bin/activate
pip install flask
```

### Method 3: Using --break-system-packages (Not Recommended)
```bash
pip3 install --break-system-packages flask
```

## Verify Installation

After installing, verify Flask is available:

```bash
python3 -c "import flask; print('Flask version:', flask.__version__)"
```

## Then Start Web Server

```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC
python3 web_search.py
```

Then open: http://localhost:5000

