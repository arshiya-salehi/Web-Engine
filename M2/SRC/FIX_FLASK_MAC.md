# Fix Flask Installation on macOS

## The Problem

You have two Python installations:
1. **Homebrew Python** (`/opt/homebrew/opt/python@3.13/bin/python3.13`) - Currently being used
2. **Anaconda Python** (`/opt/anaconda3/bin/python3`) - Has Flask installed

## Solution Options

### Option 1: Install Flask in Homebrew Python (Easiest)

```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC

# Install Flask for Homebrew Python
python3 -m pip install --user flask

# Verify
python3 -c "import flask; print('✅ Flask works!')"

# Run web server
python3 web_search.py
```

### Option 2: Use Conda Python Explicitly

```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC

# Use the conda script I created
./run_web_conda.sh
```

Or manually:
```bash
# Use conda Python
/opt/anaconda3/bin/python3 web_search.py
```

### Option 3: Activate Conda Environment

```bash
# Activate conda base environment
conda activate base

# Navigate to SRC
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC

# Run (Flask is already installed in conda)
python3 web_search.py
```

---

## Recommended: Quick Fix

Just run this one command:

```bash
cd /Users/arshiyasalehi/Desktop/CS\ 121/Web-engine/Web-Engine/M2/SRC
python3 -m pip install --user flask
```

Then:
```bash
python3 web_search.py
```

Open browser: **http://localhost:5000**

---

## Verify It Works

After installing, test:

```bash
python3 -c "import flask; print('Flask version:', flask.__version__)"
```

If you see the version number, you're good to go! ✅

