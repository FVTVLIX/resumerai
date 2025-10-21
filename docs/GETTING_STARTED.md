# Getting Started Guide

Complete beginner-friendly guide to set up and run the AI Resume Analyzer.

## Prerequisites

Before you begin, ensure you have:

1. **Python 3.11 or higher** installed
   - Check: `python --version` or `python3 --version`
   - Download from: https://www.python.org/downloads/

2. **Node.js 18 or higher** installed
   - Check: `node --version`
   - Download from: https://nodejs.org/

3. **Git** installed
   - Check: `git --version`
   - Download from: https://git-scm.com/

4. **OpenAI API Key**
   - Sign up at: https://platform.openai.com/
   - Get API key from: https://platform.openai.com/api-keys
   - Note: You'll need a paid account with credits

5. **Text Editor** (recommended)
   - VS Code: https://code.visualstudio.com/
   - Or any text editor you prefer

---

## Step-by-Step Setup

### Step 1: Clone the Repository

Open your terminal/command prompt and run:

```bash
# Navigate to where you want the project
cd ~/Projects  # or C:\Users\YourName\Projects on Windows

# Clone the repository
git clone https://github.com/FVTVLIX/resumerai.git

# Enter the project directory
cd resumerai
```

### Step 2: Set Up the Backend

```bash
# Navigate to backend directory
cd backend

# Create a virtual environment (isolates Python packages)
python -m venv venv

# Activate the virtual environment
# On macOS/Linux:
source venv/bin/activate

# On Windows (Command Prompt):
venv\Scripts\activate.bat

# On Windows (PowerShell):
venv\Scripts\Activate.ps1

# You should see (venv) in your terminal prompt now

# Install required Python packages (this takes 2-5 minutes)
pip install -r requirements.txt

# Download the spaCy language model (this takes 1-2 minutes, ~800MB)
python -m spacy download en_core_web_lg
```

### Step 3: Configure Backend Environment

```bash
# Still in the backend directory

# Copy the example environment file
cp .env.example .env

# On Windows:
copy .env.example .env

# Edit the .env file with your text editor
# You need to add your OpenAI API key

# Using VS Code:
code .env

# Or any text editor:
# - On macOS: open -a TextEdit .env
# - On Windows: notepad .env
# - On Linux: nano .env
```

In the `.env` file, update these lines:

```bash
# Change this:
OPENAI_API_KEY=your-openai-api-key-here

# To this (with your actual API key):
OPENAI_API_KEY=sk-proj-abc123...
```

Save the file and close it.

### Step 4: Set Up the Frontend

```bash
# Open a NEW terminal window/tab
# Navigate to the frontend directory
cd frontend  # from project root

# Or if you're still in backend:
cd ../frontend

# Install frontend dependencies (this takes 2-5 minutes)
npm install

# Create frontend environment file
echo "VITE_API_URL=http://localhost:5000/api" > .env

# On Windows (PowerShell):
"VITE_API_URL=http://localhost:5000/api" | Out-File -FilePath .env -Encoding utf8

# On Windows (Command Prompt):
echo VITE_API_URL=http://localhost:5000/api > .env
```

### Step 5: Start the Application

You need TWO terminal windows open:

**Terminal 1 - Backend:**
```bash
# Navigate to backend directory
cd backend

# Activate virtual environment (if not already active)
source venv/bin/activate  # macOS/Linux
# OR
venv\Scripts\activate  # Windows

# Start the backend server
python app.py

# You should see:
# * Running on http://0.0.0.0:5000
# Leave this terminal running
```

**Terminal 2 - Frontend:**
```bash
# Navigate to frontend directory
cd frontend

# Start the development server
npm run dev

# You should see:
# ➜  Local:   http://localhost:5173/
# Leave this terminal running
```

### Step 6: Open the Application

1. Open your web browser
2. Go to: **http://localhost:5173**
3. You should see the AI Resume Analyzer interface!

---

## Using the Application

### Analyzing Your First Resume

1. **Prepare a Resume**
   - Supported formats: PDF or DOCX
   - Maximum size: 5MB
   - Should contain actual resume content

2. **Upload Resume**
   - Drag and drop your resume file onto the upload area
   - OR click "Browse Files" to select a file
   - The file name and size will display after selection

3. **Start Analysis**
   - Click the "Analyze Resume" button
   - Wait 10-20 seconds for analysis to complete
   - You'll see a progress bar with status updates

4. **View Results**
   - Overall score (0-100)
   - Skills breakdown by category
   - Experience timeline
   - AI-powered suggestions for improvement
   - Content quality metrics
   - ATS optimization score

5. **Export Results**
   - Click "Export Results" to download a JSON file
   - Contains all analysis data for your records

6. **Analyze Another Resume**
   - Click "New Analysis" to start over
   - Previous results will be cleared

---

## Troubleshooting

### Common Issues

#### 1. "python: command not found"

**Solution**: Try `python3` instead of `python`:
```bash
python3 --version
python3 -m venv venv
```

#### 2. "pip: command not found"

**Solution**: Try `pip3` or install pip:
```bash
# macOS/Linux
sudo easy_install pip

# Windows
python -m ensurepip --upgrade
```

#### 3. "Permission denied" when creating virtual environment

**Solution**:
```bash
# macOS/Linux - use sudo
sudo python3 -m venv venv

# Windows - run as Administrator
```

#### 4. "Cannot activate virtual environment on Windows"

**Solution**: PowerShell execution policy issue
```powershell
# Run PowerShell as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser

# Then try activating again
venv\Scripts\Activate.ps1
```

#### 5. spaCy model download fails

**Solution**:
```bash
# Try direct download
pip install https://github.com/explosion/spacy-models/releases/download/en_core_web_lg-3.7.0/en_core_web_lg-3.7.0-py3-none-any.whl

# Or smaller model for testing
python -m spacy download en_core_web_sm
# Then update config.py: SPACY_MODEL = 'en_core_web_sm'
```

#### 6. "OpenAI API error: Unauthorized"

**Solutions**:
- Verify API key is correct in `.env`
- Check API key has credits: https://platform.openai.com/account/usage
- Ensure no extra spaces in `.env` file
- Restart backend server after changing `.env`

#### 7. CORS errors in browser console

**Solutions**:
- Check backend is running on port 5000
- Verify frontend `.env` has correct API URL
- Check `CORS_ORIGINS` in backend `.env` includes `http://localhost:5173`

#### 8. "Module not found" errors

**Solution**: Reinstall dependencies
```bash
# Backend
cd backend
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules package-lock.json
npm install
```

#### 9. Port already in use

**Backend (port 5000)**:
```bash
# Find and kill process using port 5000

# macOS/Linux
lsof -ti:5000 | xargs kill -9

# Windows
netstat -ano | findstr :5000
taskkill /PID <PID> /F
```

**Frontend (port 5173)**:
```bash
# macOS/Linux
lsof -ti:5173 | xargs kill -9

# Windows
netstat -ano | findstr :5173
taskkill /PID <PID> /F
```

#### 10. File upload fails

**Checks**:
- File size < 5MB
- File format is PDF or DOCX (not .doc, .txt, etc.)
- File is not password-protected
- File contains extractable text (not scanned image)

---

## Testing Your Setup

### Backend Health Check

Open a new terminal and run:

```bash
# Test backend API
curl http://localhost:5000/api/health

# Expected response:
# {"status":"healthy","services":{"ai":"ready","file_processor":"ready","nlp":"ready"},"version":"1.0.0"}
```

### Frontend Build Test

```bash
cd frontend
npm run build

# Should complete without errors
# Creates a 'dist' folder
```

---

## Next Steps

### Learn More

1. **Read Documentation**
   - [Architecture Guide](ARCHITECTURE.md) - Understand the system design
   - [Testing Guide](TESTING.md) - Learn how to test the application
   - [Deployment Guide](DEPLOYMENT.md) - Deploy to production

2. **Explore the Code**
   - **Backend**: Start with `backend/app.py`
   - **Services**: Check `backend/services/analyzer.py`
   - **Frontend**: Look at `frontend/src/App.jsx`

3. **Customize**
   - Modify skill categories in `backend/utils/constants.py`
   - Adjust scoring weights in `backend/models/analysis.py`
   - Change UI theme in `frontend/src/App.jsx`

### Development Tips

1. **Backend Development**
   ```bash
   # Enable auto-reload
   # In backend/.env:
   DEBUG=True

   # Backend will restart on code changes
   ```

2. **Frontend Development**
   ```bash
   # Vite automatically reloads on changes
   # Edit files in frontend/src/
   # Changes appear immediately in browser
   ```

3. **Debugging**
   ```bash
   # Backend logs
   # In backend/app.py, add:
   import logging
   logging.basicConfig(level=logging.DEBUG)

   # Frontend debugging
   # Open browser DevTools (F12)
   # Check Console tab for errors
   ```

---

## Cost Considerations

### OpenAI API Costs

- **Model**: GPT-4
- **Cost**: ~$0.03 per resume analysis
- **Monthly estimate** (for development):
  - 50 analyses: ~$1.50
  - 200 analyses: ~$6.00
  - 500 analyses: ~$15.00

### Ways to Reduce Costs

1. **Use GPT-3.5 Turbo** (cheaper, faster, but less accurate)
   ```bash
   # In backend/.env:
   OPENAI_MODEL=gpt-3.5-turbo
   ```

2. **Disable AI Suggestions** (for testing)
   ```bash
   # In backend/.env:
   ENABLE_AI_SUGGESTIONS=False
   ```

3. **Set API Limits** in OpenAI dashboard
   - Set monthly budget limit
   - Get email alerts at thresholds

---

## Getting Help

### Resources

- **GitHub Issues**: Report bugs or request features
- **Documentation**: Check `/docs` folder
- **Sample Output**: See `docs/SAMPLE_OUTPUT.md`

### Before Asking for Help

1. Check error messages carefully
2. Review troubleshooting section above
3. Ensure all prerequisites are installed
4. Verify environment variables are set correctly
5. Try restarting both servers

### Reporting Issues

Include:
- Operating system and version
- Python version
- Node.js version
- Error messages (full text)
- Steps to reproduce

---

## Success Checklist

- [ ] Python 3.11+ installed and verified
- [ ] Node.js 18+ installed and verified
- [ ] Repository cloned successfully
- [ ] Backend virtual environment created
- [ ] Backend dependencies installed
- [ ] spaCy model downloaded
- [ ] Backend .env configured with OpenAI API key
- [ ] Frontend dependencies installed
- [ ] Frontend .env created
- [ ] Backend server starts without errors
- [ ] Frontend server starts without errors
- [ ] Application opens in browser
- [ ] Can upload a test resume
- [ ] Analysis completes successfully
- [ ] Results display correctly

---

Congratulations! You now have a fully functional AI-powered resume analyzer running locally. Happy analyzing! 🎉
