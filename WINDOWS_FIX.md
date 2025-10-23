# Windows Installation Fix - python-magic Issue

## The Error You're Seeing

```
ImportError: failed to find libmagic. Check your installation
```

## What Happened

The `python-magic` library requires a system library called `libmagic` which is not available on Windows by default.

## ✅ FIXED - Two Solutions

I've updated the code to handle this automatically. Choose either solution:

---

## Solution 1: Quick Fix (Recommended)

Uninstall the broken package and reinstall with the Windows-compatible version:

```cmd
# Make sure you're in the backend folder with venv activated
cd C:\Users\Andres\desktop\codeprojects\resumerai\backend
venv\Scripts\activate.bat

# Uninstall the broken package
pip uninstall python-magic -y

# Pull the latest changes
git pull origin claude/ai-resume-analyzer-project-011CUKV68PurnKRS9pZAk1Nk

# Reinstall requirements (will use python-magic-bin on Windows)
pip install -r requirements.txt

# Now run the app
python app.py
```

**What this does:**
- Removes the broken `python-magic` package
- Installs `python-magic-bin` instead (Windows-compatible version)
- Includes the necessary Windows binary files

---

## Solution 2: Manual Install

If Solution 1 doesn't work:

```cmd
# Activate venv
venv\Scripts\activate.bat

# Uninstall python-magic
pip uninstall python-magic -y

# Install Windows-compatible version
pip install python-magic-bin

# Run the app
python app.py
```

---

## What I Fixed

### 1. Updated `requirements.txt`
Changed from:
```python
python-magic>=0.4.27
```

To:
```python
python-magic-bin>=0.4.14; platform_system == "Windows"
python-magic>=0.4.27; platform_system != "Windows"
```

This automatically installs the correct version based on your operating system.

### 2. Updated `validators.py`
Made the code handle missing `libmagic` gracefully:
```python
# Try to import magic, but don't fail if unavailable
try:
    import magic
    MAGIC_AVAILABLE = True
except (ImportError, OSError):
    # Will use extension-only validation
    MAGIC_AVAILABLE = False
```

**What this means:**
- If `libmagic` is available, it's used for extra validation
- If not available, the app still works using file extension validation
- No more crashes!

---

## Verification

After running Solution 1 or 2, verify the fix:

```cmd
# Check what's installed
pip list | findstr magic

# Should show:
# python-magic-bin    0.4.14  (on Windows)
```

Then run the app:
```cmd
python app.py
```

✅ **Success!** You should see:
```
 * Running on http://0.0.0.0:5000
```

---

## Why This Happened

`python-magic` is a Python wrapper around the `libmagic` C library, which is:
- ✅ Built-in on macOS and Linux
- ❌ **NOT** available on Windows

**Solution:** Use `python-magic-bin` which includes Windows binaries.

---

## Alternative: Disable MIME Checking (Not Recommended)

If you still have issues, you can disable MIME validation:

Edit `backend/utils/validators.py`, line 119:
```python
# Change this:
if not MAGIC_AVAILABLE:
    return True

# To this (always skip MIME check):
return True  # Skip MIME validation
```

But this is less secure, so only do this as a last resort.

---

## Next Steps

After fixing this:

1. ✅ Backend should start: `python app.py`
2. Open **NEW** Command Prompt
3. Start frontend:
   ```cmd
   cd C:\Users\Andres\desktop\codeprojects\resumerai\frontend
   npm run dev
   ```
4. Open http://localhost:5173
5. Test uploading a resume!

---

## Still Having Issues?

If you still get errors:

1. **Make sure venv is activated** (you see `(venv)` in prompt)
2. **Check Python version**: `python --version` (need 3.9+)
3. **Clear pip cache**:
   ```cmd
   pip cache purge
   pip uninstall python-magic python-magic-bin -y
   pip install python-magic-bin
   ```
4. **Start fresh**:
   ```cmd
   rmdir /s venv
   python -m venv venv
   venv\Scripts\activate.bat
   pip install -r requirements.txt
   ```

---

## Summary

The fix is simple:
1. Pull latest code
2. Reinstall requirements
3. Run the app

The code now works on Windows without `libmagic`! 🎉
