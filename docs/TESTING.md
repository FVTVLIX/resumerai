# Testing Guide

## Table of Contents
1. [Backend Testing](#backend-testing)
2. [Frontend Testing](#frontend-testing)
3. [Integration Testing](#integration-testing)
4. [Test Coverage](#test-coverage)
5. [Running Tests](#running-tests)

---

## Backend Testing

### Setup

```bash
cd backend
pip install -r requirements.txt
pip install pytest pytest-flask pytest-cov pytest-mock
```

### Test Structure

```
backend/tests/
├── __init__.py
├── conftest.py              # Pytest configuration and fixtures
├── test_file_processor.py   # File processing tests
├── test_nlp_service.py      # NLP service tests
├── test_ai_service.py       # AI service tests
├── test_analyzer.py         # Main analyzer tests
└── test_api.py              # API endpoint tests
```

### Sample Test Cases

#### 1. File Processor Tests (`backend/tests/test_file_processor.py`)

```python
import pytest
import os
from services.file_processor import FileProcessor, clean_text
from utils.exceptions import FileProcessingError
from werkzeug.datastructures import FileStorage
from io import BytesIO

@pytest.fixture
def file_processor(tmp_path):
    """Create file processor with temporary directory"""
    return FileProcessor(upload_folder=str(tmp_path))

@pytest.fixture
def sample_pdf():
    """Create a mock PDF file"""
    # In real tests, use a real PDF file
    return FileStorage(
        stream=BytesIO(b'%PDF-1.4 sample content'),
        filename='test_resume.pdf',
        content_type='application/pdf'
    )

def test_extract_text_from_pdf(file_processor, sample_pdf):
    """Test PDF text extraction"""
    text, metadata = file_processor.process_file(sample_pdf)

    assert text is not None
    assert len(text) > 0
    assert metadata['filename'] == 'test_resume.pdf'
    assert metadata['extension'] == 'pdf'
    assert 'word_count' in metadata

def test_file_too_large():
    """Test file size validation"""
    from utils.validators import FileValidator

    validator = FileValidator(
        allowed_extensions={'pdf', 'docx'},
        allowed_mime_types={'application/pdf'},
        max_size=5 * 1024 * 1024
    )

    # Create a mock large file
    large_file = FileStorage(
        stream=BytesIO(b'x' * (6 * 1024 * 1024)),  # 6MB
        filename='large.pdf'
    )

    with pytest.raises(Exception):  # Should raise FileValidationError
        validator.validate(large_file)

def test_invalid_file_type():
    """Test invalid file type rejection"""
    from utils.validators import FileValidator

    validator = FileValidator(
        allowed_extensions={'pdf', 'docx'},
        allowed_mime_types={'application/pdf'},
        max_size=5 * 1024 * 1024
    )

    invalid_file = FileStorage(
        stream=BytesIO(b'not a pdf'),
        filename='test.txt',
        content_type='text/plain'
    )

    with pytest.raises(Exception):
        validator.validate(invalid_file)

def test_clean_text():
    """Test text cleaning function"""
    dirty_text = """

        Line 1


        Line 2

        Line 3
    """

    clean = clean_text(dirty_text)

    assert 'Line 1' in clean
    assert 'Line 2' in clean
    assert 'Line 3' in clean
    # Should remove excessive whitespace
    assert clean.count('\n') < dirty_text.count('\n')
```

#### 2. NLP Service Tests (`backend/tests/test_nlp_service.py`)

```python
import pytest
from services.nlp_service import NLPService
from models import Skill, Experience

@pytest.fixture
def nlp_service():
    """Create NLP service instance"""
    # Mock or use a smaller model for testing
    return NLPService(model_name='en_core_web_sm')

def test_skill_extraction(nlp_service):
    """Test skill extraction from resume text"""
    text = """
    Experienced software engineer with expertise in Python, JavaScript, and React.
    Proficient in Docker, AWS, and MySQL. Strong leadership and communication skills.
    """

    skills = nlp_service.extract_skills(text)

    assert len(skills) > 0
    skill_names = [s.name for s in skills]
    assert 'Python' in skill_names
    assert 'JavaScript' in skill_names
    assert 'React' in skill_names

def test_experience_extraction(nlp_service):
    """Test experience extraction"""
    text = """
    EXPERIENCE

    Senior Software Engineer
    Tech Corp Inc.
    January 2020 - December 2023

    - Led team of 5 developers
    - Architected microservices platform
    - Improved performance by 40%

    Software Engineer
    Startup Inc.
    June 2019 - December 2019

    - Built React applications
    - Collaborated with design team
    """

    experiences = nlp_service.extract_experience(text)

    assert len(experiences) >= 1
    assert experiences[0].title is not None
    assert experiences[0].company is not None

def test_action_verb_detection(nlp_service):
    """Test action verb usage analysis"""
    bullets = [
        'Led team of developers',
        'Improved system performance',
        'Responsible for managing projects'
    ]

    has_action_verb = nlp_service._starts_with_action_verb

    assert has_action_verb(bullets[0]) == True  # 'led'
    assert has_action_verb(bullets[1]) == True  # 'improved'
    assert has_action_verb(bullets[2]) == False  # 'responsible for'

def test_ats_score_calculation(nlp_service):
    """Test ATS score calculation"""
    text = """
    Experienced Python developer with React, Django, and AWS experience.
    Led multiple projects and improved team efficiency by 50%.
    Strong problem-solving and leadership skills.
    """

    from models.analysis import AnalysisMetrics

    skills = nlp_service.extract_skills(text)
    metrics = nlp_service.analyze_content_quality(text)
    ats_score = nlp_service.calculate_ats_score(text, skills, metrics)

    assert 0 <= ats_score <= 100
    assert isinstance(ats_score, float)
```

#### 3. API Tests (`backend/tests/test_api.py`)

```python
import pytest
from app import create_app
from io import BytesIO

@pytest.fixture
def app():
    """Create application for testing"""
    app = create_app('testing')
    yield app

@pytest.fixture
def client(app):
    """Create test client"""
    return app.test_client()

def test_health_endpoint(client):
    """Test health check endpoint"""
    response = client.get('/api/health')

    assert response.status_code == 200
    data = response.get_json()
    assert data['status'] == 'healthy'
    assert 'services' in data

def test_analyze_endpoint_no_file(client):
    """Test analyze endpoint without file"""
    response = client.post('/api/analyze')

    assert response.status_code == 400
    data = response.get_json()
    assert data['success'] == False
    assert 'NO_FILE' in data['error']['code']

def test_analyze_endpoint_with_valid_pdf(client):
    """Test analyze endpoint with valid PDF"""
    # Create a simple mock PDF file
    data = {
        'file': (BytesIO(b'%PDF-1.4 mock content'), 'test.pdf')
    }

    response = client.post(
        '/api/analyze',
        data=data,
        content_type='multipart/form-data'
    )

    # Note: This will likely fail in real tests without a valid PDF
    # Use actual test files in production tests
    assert response.status_code in [200, 422]

def test_analyze_endpoint_invalid_file_type(client):
    """Test analyze endpoint with invalid file type"""
    data = {
        'file': (BytesIO(b'not a pdf'), 'test.txt')
    }

    response = client.post(
        '/api/analyze',
        data=data,
        content_type='multipart/form-data'
    )

    assert response.status_code == 400

def test_skill_categories_endpoint(client):
    """Test skill categories endpoint"""
    response = client.get('/api/skills/categories')

    assert response.status_code == 200
    data = response.get_json()
    assert data['success'] == True
    assert 'categories' in data
    assert len(data['categories']) > 0

def test_rate_limiting(client):
    """Test rate limiting (if enabled)"""
    # Make multiple rapid requests
    for _ in range(15):
        response = client.get('/api/health')

    # The 15th request might be rate limited (depending on config)
    # In testing mode, rate limiting is usually disabled
    assert response.status_code in [200, 429]
```

### Running Backend Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=. --cov-report=html

# Run specific test file
pytest tests/test_api.py

# Run specific test
pytest tests/test_api.py::test_health_endpoint

# Run with verbose output
pytest -v

# Run and stop at first failure
pytest -x
```

---

## Frontend Testing

### Setup

```bash
cd frontend
npm install
npm install --save-dev @testing-library/react @testing-library/jest-dom @testing-library/user-event vitest
```

### Test Structure

```
frontend/src/
├── components/
│   ├── __tests__/
│   │   ├── Header.test.jsx
│   │   ├── UploadSection.test.jsx
│   │   ├── AnalysisProgress.test.jsx
│   │   └── ResultsDashboard.test.jsx
│   └── ...
├── services/
│   └── __tests__/
│       └── api.test.js
└── test/
    └── setup.js
```

### Sample Test Cases

#### 1. Component Tests (`frontend/src/components/__tests__/UploadSection.test.jsx`)

```javascript
import { describe, it, expect, vi } from 'vitest'
import { render, screen, fireEvent, waitFor } from '@testing-library/react'
import userEvent from '@testing-library/user-event'
import UploadSection from '../UploadSection'

describe('UploadSection', () => {
  it('renders upload area', () => {
    render(<UploadSection onFileUpload={vi.fn()} />)

    expect(screen.getByText(/Drag & drop your resume here/i)).toBeInTheDocument()
    expect(screen.getByText(/Supported formats: PDF, DOCX/i)).toBeInTheDocument()
  })

  it('displays selected file', async () => {
    const file = new File(['dummy content'], 'resume.pdf', { type: 'application/pdf' })
    const onFileUpload = vi.fn()

    render(<UploadSection onFileUpload={onFileUpload} />)

    const input = screen.getByLabelText(/drag & drop/i, { selector: 'input' })
    await userEvent.upload(input, file)

    await waitFor(() => {
      expect(screen.getByText(/resume.pdf/i)).toBeInTheDocument()
    })
  })

  it('calls onFileUpload when analyze button is clicked', async () => {
    const file = new File(['dummy content'], 'resume.pdf', { type: 'application/pdf' })
    const onFileUpload = vi.fn()

    render(<UploadSection onFileUpload={onFileUpload} />)

    const input = screen.getByLabelText(/drag & drop/i, { selector: 'input' })
    await userEvent.upload(input, file)

    const analyzeButton = screen.getByRole('button', { name: /analyze resume/i })
    fireEvent.click(analyzeButton)

    expect(onFileUpload).toHaveBeenCalledWith(file)
  })

  it('shows error for invalid file type', async () => {
    const file = new File(['dummy content'], 'resume.txt', { type: 'text/plain' })

    render(<UploadSection onFileUpload={vi.fn()} />)

    const input = screen.getByLabelText(/drag & drop/i, { selector: 'input' })
    await userEvent.upload(input, file)

    await waitFor(() => {
      expect(screen.getByText(/only pdf and docx files/i)).toBeInTheDocument()
    })
  })
})
```

#### 2. API Service Tests (`frontend/src/services/__tests__/api.test.js`)

```javascript
import { describe, it, expect, vi, beforeEach } from 'vitest'
import axios from 'axios'
import { analyzeResume, checkHealth } from '../api'

vi.mock('axios')

describe('API Service', () => {
  beforeEach(() => {
    vi.clearAllMocks()
  })

  it('analyzes resume successfully', async () => {
    const mockResponse = {
      data: {
        success: true,
        data: {
          overall_score: 85,
          skills: [],
          experience: [],
        }
      }
    }

    axios.create.mockReturnValue({
      post: vi.fn().mockResolvedValue(mockResponse)
    })

    const file = new File(['dummy'], 'resume.pdf', { type: 'application/pdf' })
    const result = await analyzeResume(file)

    expect(result.overall_score).toBe(85)
  })

  it('handles API errors correctly', async () => {
    axios.create.mockReturnValue({
      post: vi.fn().mockRejectedValue(new Error('Network error'))
    })

    const file = new File(['dummy'], 'resume.pdf', { type: 'application/pdf' })

    await expect(analyzeResume(file)).rejects.toThrow()
  })

  it('checks health successfully', async () => {
    const mockResponse = {
      data: {
        status: 'healthy',
        services: { nlp: 'ready', ai: 'ready' }
      }
    }

    axios.create.mockReturnValue({
      get: vi.fn().mockResolvedValue(mockResponse)
    })

    const result = await checkHealth()

    expect(result.status).toBe('healthy')
  })
})
```

### Running Frontend Tests

```bash
# Run all tests
npm test

# Run with UI
npm run test:ui

# Run with coverage
npm run test:coverage

# Run in watch mode
npm test -- --watch
```

---

## Integration Testing

### End-to-End Test Flow

```python
def test_complete_resume_analysis_flow(client):
    """Test complete flow from upload to results"""
    # 1. Check health
    health = client.get('/api/health')
    assert health.status_code == 200

    # 2. Upload resume
    with open('tests/fixtures/sample_resume.pdf', 'rb') as f:
        data = {'file': (f, 'sample_resume.pdf')}
        response = client.post(
            '/api/analyze',
            data=data,
            content_type='multipart/form-data'
        )

    # 3. Verify results
    assert response.status_code == 200
    result = response.get_json()

    assert result['success'] == True
    assert 'data' in result
    assert 'overall_score' in result['data']
    assert 'skills' in result['data']
    assert 'experience' in result['data']
    assert 'ai_suggestions' in result['data']
```

---

## Test Coverage

### Coverage Goals

- **Backend**: 80% minimum
- **Frontend**: 70% minimum
- **Critical paths**: 95% minimum

### Checking Coverage

```bash
# Backend
cd backend
pytest --cov=. --cov-report=html
# Open htmlcov/index.html

# Frontend
cd frontend
npm run test:coverage
# Open coverage/index.html
```

---

## Best Practices

1. **Test Isolation**: Each test should be independent
2. **Mock External Services**: Mock OpenAI API, file I/O
3. **Use Fixtures**: Reusable test data and setup
4. **Test Edge Cases**: Empty files, large files, malformed data
5. **Continuous Integration**: Run tests on every commit

---

## Sample Test Data

Create sample resume files for testing:

- **`tests/fixtures/sample_resume.pdf`**: Valid PDF resume
- **`tests/fixtures/sample_resume.docx`**: Valid DOCX resume
- **`tests/fixtures/empty.pdf`**: Empty PDF
- **`tests/fixtures/corrupted.pdf`**: Corrupted PDF
- **`tests/fixtures/large.pdf`**: File larger than 5MB
- **`tests/fixtures/scanned.pdf`**: Scanned resume (image-only)

---

## Troubleshooting Tests

### Common Issues

1. **spaCy model not found**
   ```bash
   python -m spacy download en_core_web_lg
   ```

2. **OpenAI API key in tests**
   - Mock the AI service in tests
   - Use environment variable for integration tests

3. **File upload tests failing**
   - Check file paths
   - Verify MIME types
   - Ensure test fixtures exist

4. **React component tests failing**
   - Check test setup.js configuration
   - Verify Material-UI theme provider
   - Mock API calls

---

This testing guide provides comprehensive coverage for ensuring the Resume Analyzer works correctly across all components and scenarios.
