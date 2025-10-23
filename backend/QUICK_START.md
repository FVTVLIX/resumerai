# Backend Quick Start Guide

## The Error You're Seeing

```
ModuleNotFoundError: No module named 'flask'
```

**What it means**: Flask is not installed in your current Python environment.

**Why it happens**: You need to activate the virtual environment first!

---

## Step-by-Step Fix (Windows)

Since you're on Windows (`C:\Users\Andres\desktop\...`), follow these steps:

### 1. Open Command Prompt or PowerShell
Navigate to the backend folder:
```cmd
cd C:\Users\Andres\desktop\codeprojects\resumerai\backend
```

### 2. Create Virtual Environment (if not done yet)
```cmd
python -m venv venv
```

You should see a new `venv` folder created.

### 3. Activate the Virtual Environment

**For Command Prompt:**
```cmd
venv\Scripts\activate.bat
```

**For PowerShell:**
```powershell
venv\Scripts\Activate.ps1
```

**For Git Bash:**
```bash
source venv/Scripts/activate
```

✅ **Success indicator**: You'll see `(venv)` at the start of your command prompt:
```
(venv) C:\Users\Andres\desktop\codeprojects\resumerai\backend>
```

### 4. Install Requirements
Now that the virtual environment is active:
```cmd
pip install -r requirements.txt
```

This will take 2-5 minutes.

### 5. Download spaCy Model
```cmd
python -m spacy download en_core_web_lg
```

This will take 1-2 minutes (~800MB download).

### 6. Create .env File
```cmd
copy .env.example .env
```

Then edit `.env` with Notepad:
```cmd
notepad .env
```

Add your OpenAI API key:
```
OPENAI_API_KEY=sk-your-actual-key-here
```

Save and close.

### 7. Run the App
```cmd
python app.py
```

✅ **Success!** You should see:
```
 * Running on http://0.0.0.0:5000
```

---

## Troubleshooting

### Issue: "cannot be loaded because running scripts is disabled"

**Error:**
```
venv\Scripts\Activate.ps1 cannot be loaded because running scripts is disabled on this system
```

**Fix (PowerShell):**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating again:
```powershell
venv\Scripts\Activate.ps1
```

### Issue: "python: command not found"

**Fix:** Try `python3` or `py` instead:
```cmd
py -m venv venv
py -m pip install -r requirements.txt
py app.py
```

### Issue: Virtual environment not activating

**Check if venv exists:**
```cmd
dir venv
```

If it doesn't exist, create it:
```cmd
python -m venv venv
```

**Still not working?** Delete and recreate:
```cmd
rmdir /s venv
python -m venv venv
venv\Scripts\activate.bat
```

### Issue: pip install fails

**Upgrade pip first:**
```cmd
python -m pip install --upgrade pip
```

Then try again:
```cmd
pip install -r requirements.txt
```

---

## For macOS/Linux Users

### 1. Navigate to backend
```bash
cd /path/to/resumerai/backend
```

### 2. Create virtual environment
```bash
python3 -m venv venv
```

### 3. Activate virtual environment
```bash
source venv/bin/activate
```

You'll see `(venv)` in your prompt.

### 4. Install requirements
```bash
pip install -r requirements.txt
```

### 5. Download spaCy model
```bash
python -m spacy download en_core_web_lg
```

### 6. Create .env file
```bash
cp .env.example .env
nano .env  # or use your preferred editor
```

Add your OpenAI API key and save.

### 7. Run the app
```bash
python app.py
```

---

## Verification Checklist

Before running `python app.py`, verify:

- [ ] You're in the `backend` folder
- [ ] Virtual environment is activated (you see `(venv)` in prompt)
- [ ] Requirements installed (`pip list` shows flask, spacy, etc.)
- [ ] spaCy model downloaded (try `python -c "import spacy; spacy.load('en_core_web_lg')"`)
- [ ] `.env` file exists with your OpenAI API key
- [ ] Port 5000 is not already in use

## Common Mistakes

### ❌ Running without activating venv
```cmd
# WRONG - No (venv) in prompt
C:\...\backend> python app.py
ModuleNotFoundError: No module named 'flask'
```

### ✅ Correct way
```cmd
# RIGHT - (venv) shows it's activated
(venv) C:\...\backend> python app.py
 * Running on http://0.0.0.0:5000
```

### ❌ Installing packages globally
```cmd
# WRONG - Don't do this!
pip install flask  # This installs globally, not in venv
```

### ✅ Correct way
```cmd
# RIGHT - Activate venv first
venv\Scripts\activate.bat
pip install -r requirements.txt  # Installs in venv
```

---

## Quick Command Reference

### Windows (Command Prompt)
```cmd
cd backend
python -m venv venv
venv\Scripts\activate.bat
pip install -r requirements.txt
python -m spacy download en_core_web_lg
copy .env.example .env
python app.py
```

### Windows (PowerShell)
```powershell
cd backend
python -m venv venv
venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m spacy download en_core_web_lg
copy .env.example .env
python app.py
```

### macOS/Linux
```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python -m spacy download en_core_web_lg
cp .env.example .env
python app.py
```

---

## Still Having Issues?

### Check Python version
```cmd
python --version
```
Need Python 3.9+ (3.11 recommended)

### Check if Flask is installed
```cmd
pip list | findstr Flask
```
Should show Flask and flask-cors

### Check virtual environment
```cmd
where python
```
Should point to `venv\Scripts\python.exe`

### Start fresh
```cmd
rmdir /s venv
python -m venv venv
venv\Scripts\activate.bat
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Success!

When everything works, you should see:

```
 * Serving Flask app 'app'
 * Debug mode: on
WARNING: This is a development server. Do not use it in a production deployment.
 * Running on http://0.0.0.0:5000
Press CTRL+C to quit
 * Restarting with stat
 * Debugger is active!
```

Now open another terminal and start the frontend!

---

## Next Steps

1. ✅ Backend running on http://localhost:5000
2. Open **new terminal/command prompt**
3. Navigate to `frontend` folder
4. Run `npm run dev`
5. Open http://localhost:5173 in browser
6. Upload a resume and test!

---

**Need more help?** Check `INSTALL_TROUBLESHOOTING.md` in the root folder.
