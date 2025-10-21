# Installation Troubleshooting

## Common Issues and Solutions

### Issue: "Could not find a version that satisfies the requirement"

This usually happens when package versions are outdated or incompatible with your Python version.

**Solution**: The requirements.txt has been updated to use flexible version ranges (>=) instead of exact versions (==).

### Updated Installation Steps

```bash
# 1. Ensure you have Python 3.9+ (3.11 recommended)
python --version

# 2. Create and activate virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Upgrade pip to latest version
pip install --upgrade pip

# 4. Install requirements
pip install -r requirements.txt

# 5. Download spaCy model
python -m spacy download en_core_web_lg
```

### If Installation Still Fails

Try installing in stages:

```bash
# Stage 1: Core Flask dependencies
pip install Flask flask-cors flask-limiter python-dotenv Werkzeug gunicorn

# Stage 2: File processing
pip install PyPDF2 pdfplumber python-docx pdfminer.six

# Stage 3: NLP (this is the big one)
pip install spacy nltk

# Stage 4: AI
pip install openai

# Stage 5: Utilities
pip install marshmallow python-dateutil

# Stage 6: Development tools (optional)
pip install pytest pytest-flask pytest-cov pytest-mock black flake8

# Finally: Download spaCy model
python -m spacy download en_core_web_lg
```

### python-magic Installation Issues

If `python-magic` fails to install:

**On macOS:**
```bash
brew install libmagic
pip install python-magic
```

**On Ubuntu/Debian:**
```bash
sudo apt-get install libmagic1
pip install python-magic
```

**On Windows:**
```bash
# Install python-magic-bin instead
pip install python-magic-bin
```

Then update `backend/services/file_processor.py` line 8:
```python
# Change from:
import magic

# To (on Windows):
import magic
from magic import Magic
```

### Minimal Installation (No AI Suggestions)

If you want to test without OpenAI:

```bash
pip install Flask flask-cors python-dotenv
pip install PyPDF2 pdfplumber python-docx
pip install spacy
python -m spacy download en_core_web_sm  # Smaller model
```

Then in `.env`:
```bash
ENABLE_AI_SUGGESTIONS=False
SPACY_MODEL=en_core_web_sm
```

### Python Version Compatibility

- **Recommended**: Python 3.11
- **Minimum**: Python 3.9
- **Maximum**: Python 3.12

Check compatibility:
```bash
python --version
```

If you have multiple Python versions:
```bash
python3.11 -m venv venv
# or
python3.9 -m venv venv
```

### Virtual Environment Issues

If virtual environment activation fails:

**On Windows PowerShell:**
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**On macOS/Linux:**
```bash
chmod +x venv/bin/activate
source venv/bin/activate
```

### Verification

After installation, verify everything is working:

```bash
python -c "import flask; print('Flask OK')"
python -c "import spacy; print('spaCy OK')"
python -c "import PyPDF2; print('PyPDF2 OK')"
python -c "import docx; print('python-docx OK')"
python -c "import openai; print('OpenAI OK')"
```

### Still Having Issues?

1. Clear pip cache: `pip cache purge`
2. Remove virtual environment and recreate: `rm -rf venv && python -m venv venv`
3. Update pip: `pip install --upgrade pip setuptools wheel`
4. Try using conda instead: `conda create -n resumerai python=3.11`

### Contact

If you still encounter issues, please provide:
- Python version (`python --version`)
- Operating system
- Full error message
- Output of `pip list`
