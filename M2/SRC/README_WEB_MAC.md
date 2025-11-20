# Running Web Interface on macOS - SIMPLE SOLUTION

## ✅ The Easiest Way

Since Flask is already installed in your conda environment, just use conda Python directly:

### Method 1: Use the Simple Script (Easiest)

```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC
./RUN_WEB_SIMPLE.sh
```

### Method 2: Use Conda Python Directly

```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC
/opt/anaconda3/bin/python3 web_search.py
```

### Method 3: Activate Conda First

```bash
# Activate conda
conda activate base

# Navigate to SRC
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC

# Run (Flask is already installed)
python3 web_search.py
```

---

## What You'll See

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

---

## Then Open Browser

Go to: **http://localhost:5000**

You'll see a beautiful web interface where you can:
- Enter search queries
- Get clickable results
- Click URLs to open them in new tabs

---

## Stop the Server

Press `Ctrl+C` in the terminal.

---

## That's It! 🎉

The web interface should work perfectly now using conda Python!

