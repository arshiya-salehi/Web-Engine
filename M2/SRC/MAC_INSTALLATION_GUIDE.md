# Installing Flask on macOS - Step by Step

## Option 1: Use Existing Virtual Environment (Recommended)

The M2 directory already has a virtual environment. Use it:

```bash
# Navigate to M2 directory
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2

# Activate virtual environment
source venv/bin/activate

# Install Flask
pip install flask

# Navigate to SRC
cd SRC

# Run web server
python3 web_search.py
```

## Option 2: Use the Mac-Friendly Script

I've created a script that handles everything automatically:

```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC
./run_web_mac.sh
```

This script will:
- Use or create a virtual environment
- Install Flask automatically
- Start the web server

## Option 3: If Using Conda (Anaconda/Miniconda)

Since you're using conda (I see "base" in your terminal), you can use conda:

```bash
# Install Flask with conda
conda install flask

# Or use pip in conda environment
pip install flask

# Then run
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC
python3 web_search.py
```

## Option 4: Manual Installation with --user flag

```bash
pip3 install --user flask
```

Then verify:
```bash
python3 -c "import flask; print('Flask installed!')"
```

## Quick Test

After installation, test if Flask works:

```bash
python3 -c "import flask; print('✅ Flask version:', flask.__version__)"
```

## Then Start the Web Server

```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC
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
```

Then open your browser and go to: **http://localhost:5000**

## Troubleshooting

### If you get "ModuleNotFoundError: No module named 'flask'"

Try one of these:

1. **Use virtual environment** (Best):
   ```bash
   cd M2
   source venv/bin/activate
   pip install flask
   cd SRC
   python3 web_search.py
   ```

2. **Use conda**:
   ```bash
   conda install flask
   ```

3. **Use --user flag**:
   ```bash
   pip3 install --user flask
   ```

### If port 5000 is already in use

Change the port in `web_search.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Use port 5001 instead
```

## Recommended: Use the Script

The easiest way is to use the Mac-friendly script:

```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC
./run_web_mac.sh
```

This handles everything automatically! 🚀

