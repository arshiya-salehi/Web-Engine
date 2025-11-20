# Quick Start for macOS - Web Interface

## ✅ Good News!

Flask is **already installed** in your conda environment! You can run the web interface directly.

## Simple Steps:

### 1. Navigate to SRC directory

```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC
```

### 2. Run the web server

```bash
python3 web_search.py
```

You should see:
```
Initializing search engine...
Loaded 1212 document mappings
Loading index into memory...
Index loaded: 13126 unique terms
Search engine ready!

============================================================
Web Search Interface
============================================================
Starting web server...
Open your browser and go to: http://localhost:5000
Press Ctrl+C to stop the server
============================================================

 * Running on http://0.0.0.0:5000
```

### 3. Open your browser

Go to: **http://localhost:5000**

### 4. Start searching!

- Enter a query in the search box
- Click "Search" or press Enter
- Click any result URL to open it in a new tab

---

## That's it! 🎉

The web interface should work now. Flask is already installed in your conda environment.

---

## If You Get an Error

If you still get "ModuleNotFoundError", try:

```bash
# Make sure you're using the conda Python
which python3

# If needed, install Flask in conda
conda install flask

# Or use pip in conda
pip install flask
```

---

## Stop the Server

Press `Ctrl+C` in the terminal to stop the web server.

---

**Enjoy your web-based search engine! 🌐**

