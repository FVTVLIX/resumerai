# System Architecture & Design

## Architecture Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         USER INTERFACE                       │
│                    (React + shadcn/ui)                       │
└─────────────────────────────────────────────────────────────┘
                              │
                              │ HTTPS/REST
                              ▼
┌─────────────────────────────────────────────────────────────┐
│                        API GATEWAY                           │
│                      (Flask + CORS)                          │
└─────────────────────────────────────────────────────────────┘
                              │
                    ┌─────────┴─────────┐
                    │                   │
                    ▼                   ▼
        ┌──────────────────┐  ┌──────────────────┐
        │  File Processing │  │  Analysis Engine │
        │    Service       │  │    Service       │
        └──────────────────┘  └──────────────────┘
                    │                   │
                    ▼                   ▼
        ┌──────────────────┐  ┌──────────────────┐
        │  Text Extraction │  │   NLP Processor  │
        │  (PDF/DOCX)      │  │   (spaCy/NLTK)   │
        └──────────────────┘  └──────────────────┘
                                        │
                                        ▼
                              ┌──────────────────┐
                              │   AI Feedback    │
                              │  (OpenAI GPT-4)  │
                              └──────────────────┘
```

## Backend Architecture

### Component Structure

```
backend/
│
├── app.py                    # Main Flask application
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
│
├── api/
│   ├── __init__.py
│   ├── routes.py            # API endpoints
│   └── validators.py        # Request validation
│
├── services/
│   ├── __init__.py
│   ├── file_processor.py    # File upload & validation
│   ├── text_extractor.py    # PDF/DOCX text extraction
│   ├── nlp_analyzer.py      # NLP processing
│   ├── scoring_engine.py    # Resume scoring logic
│   └── ai_feedback.py       # OpenAI integration
│
├── models/
│   ├── __init__.py
│   ├── resume.py            # Resume data model
│   └── analysis_result.py   # Analysis result model
│
├── utils/
│   ├── __init__.py
│   ├── validators.py        # Utility validators
│   ├── helpers.py           # Helper functions
│   └── constants.py         # Constants and configs
│
└── tests/
    ├── __init__.py
    ├── test_api.py
    ├── test_extractors.py
    └── test_analyzers.py
```

### API Endpoints Design

#### 1. Upload Resume
```
POST /api/v1/upload
Content-Type: multipart/form-data

Request Body:
{
  "file": <binary>,
  "job_role": "Software Engineer" (optional),
  "experience_level": "mid" (optional)
}

Response:
{
  "success": true,
  "file_id": "uuid-string",
  "message": "File uploaded successfully"
}
```

#### 2. Analyze Resume
```
POST /api/v1/analyze
Content-Type: application/json

Request Body:
{
  "file_id": "uuid-string",
  "analysis_type": "comprehensive" | "quick" | "ats"
}

Response:
{
  "success": true,
  "analysis": {
    "overall_score": 78,
    "sections": {
      "contact": { "score": 90, "issues": [] },
      "experience": { "score": 75, "issues": [...] },
      "skills": { "score": 80, "issues": [...] },
      "education": { "score": 85, "issues": [] }
    },
    "extracted_data": {
      "name": "John Doe",
      "email": "john@example.com",
      "phone": "+1234567890",
      "skills": ["Python", "JavaScript", "React"],
      "experience_years": 5,
      "education": [...]
    },
    "ats_score": 82,
    "keywords": {
      "found": ["Python", "React", "API"],
      "missing": ["Docker", "Kubernetes"]
    }
  }
}
```

#### 3. Get AI Suggestions
```
POST /api/v1/suggestions
Content-Type: application/json

Request Body:
{
  "file_id": "uuid-string",
  "analysis_data": { ... },
  "target_role": "Senior Developer"
}

Response:
{
  "success": true,
  "suggestions": {
    "general": ["Add quantifiable achievements", ...],
    "skills": ["Consider adding cloud certifications", ...],
    "experience": ["Use action verbs in descriptions", ...],
    "format": ["Use bullet points consistently", ...]
  },
  "priority_items": [...]
}
```

#### 4. Health Check
```
GET /api/v1/health

Response:
{
  "status": "healthy",
  "version": "1.0.0",
  "timestamp": "2025-10-19T10:00:00Z"
}
```

### NLP Processing Pipeline

```
Input Text
    │
    ▼
┌─────────────────────┐
│  Pre-processing     │
│  - Remove noise     │
│  - Normalize text   │
│  - Tokenization     │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Entity Recognition │
│  - Name extraction  │
│  - Contact info     │
│  - Dates            │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Skill Extraction   │
│  - Keyword matching │
│  - Contextual ML    │
│  - Categorization   │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Section Detection  │
│  - Experience       │
│  - Education        │
│  - Skills           │
│  - Projects         │
└─────────────────────┘
    │
    ▼
┌─────────────────────┐
│  Scoring & Analysis │
│  - Completeness     │
│  - Keyword density  │
│  - ATS compatibility│
└─────────────────────┘
    │
    ▼
Structured Output
```

## Frontend Architecture

### Component Hierarchy

```
App
│
├── Layout
│   ├── Header
│   └── Footer
│
├── Pages
│   ├── HomePage
│   │   ├── HeroSection
│   │   ├── FeaturesSection
│   │   └── CTASection
│   │
│   ├── AnalyzerPage
│   │   ├── UploadSection
│   │   │   ├── FileDropzone
│   │   │   └── FilePreview
│   │   │
│   │   ├── AnalysisSection
│   │   │   ├── ProcessingIndicator
│   │   │   └── ProgressSteps
│   │   │
│   │   └── ResultsSection
│   │       ├── ScoreCard
│   │       ├── SectionBreakdown
│   │       ├── SkillsList
│   │       ├── SuggestionsPanel
│   │       └── DownloadButton
│   │
│   └── AboutPage
│
└── Components (shadcn/ui)
    ├── Button
    ├── Card
    ├── Badge
    ├── Progress
    ├── Alert
    ├── Tabs
    └── Dialog
```

### State Management

```javascript
// Application State Structure
{
  // File Upload State
  file: {
    data: File | null,
    id: string | null,
    uploading: boolean,
    uploaded: boolean,
    error: string | null
  },
  
  // Analysis State
  analysis: {
    processing: boolean,
    completed: boolean,
    progress: number,
    data: {
      overall_score: number,
      sections: {},
      extracted_data: {},
      ats_score: number,
      keywords: {}
    },
    error: string | null
  },
  
  // Suggestions State
  suggestions: {
    loading: boolean,
    data: {
      general: [],
      skills: [],
      experience: [],
      format: []
    },
    error: string | null
  },
  
  // UI State
  ui: {
    currentStep: 'upload' | 'analyzing' | 'results',
    activeTab: string,
    showDownload: boolean
  }
}
```

### UI/UX Design Principles

1. **Progressive Disclosure**: Show information gradually as analysis progresses
2. **Visual Feedback**: Clear loading states and progress indicators
3. **Error Handling**: Friendly error messages with recovery options
4. **Accessibility**: ARIA labels, keyboard navigation, screen reader support
5. **Responsive Design**: Mobile-first approach, breakpoints at 640px, 768px, 1024px
6. **Performance**: Code splitting, lazy loading, optimized images

### Color Scheme & Design Tokens

```css
/* Primary Colors */
--primary: 222.2 47.4% 11.2%
--primary-foreground: 210 40% 98%

/* Accent Colors */
--accent-success: 142 76% 36%
--accent-warning: 38 92% 50%
--accent-error: 0 84% 60%
--accent-info: 221 83% 53%

/* Score Colors */
--score-excellent: 142 76% 36%  /* 90-100 */
--score-good: 142 71% 45%       /* 75-89 */
--score-average: 38 92% 50%     /* 60-74 */
--score-poor: 0 84% 60%         /* 0-59 */
```

## Data Flow Diagram

```
┌─────────────┐
│    User     │
└──────┬──────┘
       │
       │ 1. Upload Resume (PDF/DOCX)
       ▼
┌─────────────────────────────────────┐
│          Frontend (React)            │
│  - Validate file type & size         │
│  - Show upload progress              │
└──────────────┬──────────────────────┘
               │
               │ 2. POST /api/v1/upload
               ▼
┌─────────────────────────────────────┐
│         Backend (Flask)              │
│  - Receive file                      │
│  - Save temporarily                  │
│  - Return file_id                    │
└──────────────┬──────────────────────┘
               │
               │ 3. POST /api/v1/analyze
               ▼
┌─────────────────────────────────────┐
│      Text Extraction Service         │
│  - Parse PDF/DOCX                    │
│  - Extract raw text                  │
│  - Preserve structure                │
└──────────────┬──────────────────────┘
               │
               │ 4. Extracted Text
               ▼
┌─────────────────────────────────────┐
│       NLP Analysis Service           │
│  - Named Entity Recognition          │
│  - Skill Extraction                  │
│  - Section Detection                 │
│  - Experience Parsing                │
└──────────────┬──────────────────────┘
               │
               │ 5. Structured Data
               ▼
┌─────────────────────────────────────┐
│       Scoring Engine                 │
│  - Calculate section scores          │
│  - ATS compatibility check           │
│  - Keyword analysis                  │
│  - Overall scoring                   │
└──────────────┬──────────────────────┘
               │
               │ 6. Analysis Results
               ▼
┌─────────────────────────────────────┐
│      AI Feedback Service             │
│  - GPT-4 API call                    │
│  - Generate suggestions              │
│  - Prioritize recommendations        │
└──────────────┬──────────────────────┘
               │
               │ 7. Complete Analysis
               ▼
┌─────────────────────────────────────┐
│          Frontend (React)            │
│  - Display scores & charts           │
│  - Show suggestions                  │
│  - Enable report download            │
└──────────────┬──────────────────────┘
               │
               │ 8. View Results
               ▼
┌─────────────┐
│    User     │
└─────────────┘
```

## Security Architecture

### Authentication & Authorization
- No user authentication required for MVP
- Rate limiting by IP address
- File upload restrictions

### Data Protection
- Temporary file storage only
- Automatic cleanup after 1 hour
- No database storage of resume content
- HTTPS encryption in transit

### Input Validation
- File type whitelist (PDF, DOCX only)
- File size limit (5MB)
- Malware scanning (future)
- Input sanitization

## Scalability Considerations

### Horizontal Scaling
- Stateless API design
- Load balancer distribution
- Container orchestration (Kubernetes)

### Performance Optimization
- Caching of AI responses
- Async processing for long operations
- CDN for static assets
- Database indexing (future)

### Monitoring & Logging
- Application performance monitoring
- Error tracking and alerting
- Usage analytics
- API endpoint metrics