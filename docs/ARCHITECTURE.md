# System Architecture Documentation

## Table of Contents
1. [High-Level Architecture](#high-level-architecture)
2. [Backend Architecture](#backend-architecture)
3. [API Structure](#api-structure)
4. [Data Flow](#data-flow)
5. [Component Interactions](#component-interactions)
6. [Database Schema](#database-schema)

---

## High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                          USER INTERFACE                          │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │   Upload     │  │   Analysis   │  │   Results    │          │
│  │   Component  │  │   Progress   │  │   Dashboard  │          │
│  └──────────────┘  └──────────────┘  └──────────────┘          │
│                                                                   │
│                    React Frontend (Port 5173)                    │
└───────────────────────────┬─────────────────────────────────────┘
                            │ HTTPS/REST API
                            │ JSON
┌───────────────────────────┴─────────────────────────────────────┐
│                      API GATEWAY LAYER                           │
│                                                                   │
│  ┌──────────────────────────────────────────────────────────┐  │
│  │              Flask Application (Port 5000)                │  │
│  │                                                            │  │
│  │  • CORS Handler                                           │  │
│  │  • Rate Limiter (10 req/min)                             │  │
│  │  • Request Validator                                      │  │
│  │  • Error Handler                                          │  │
│  └──────────────────────────────────────────────────────────┘  │
│                                                                   │
└───────────────────────────┬─────────────────────────────────────┘
                            │
        ┌───────────────────┼───────────────────┐
        │                   │                   │
┌───────┴────────┐  ┌──────┴──────┐  ┌────────┴─────────┐
│  File Service  │  │ NLP Service │  │   AI Service     │
│                │  │             │  │                  │
│ • Upload       │  │ • spaCy     │  │ • OpenAI GPT-4   │
│ • Validate     │  │ • BERT      │  │ • Prompt Eng.    │
│ • Parse PDF    │  │ • Skills    │  │ • Suggestions    │
│ • Parse DOCX   │  │ • Entities  │  │                  │
└────────────────┘  └─────────────┘  └──────────────────┘
        │                   │                   │
        │                   │                   │
        └───────────────────┼───────────────────┘
                            │
                    ┌───────┴────────┐
                    │  Analysis      │
                    │  Orchestrator  │
                    └────────────────┘
                            │
                    ┌───────┴────────┐
                    │  Response      │
                    │  Builder       │
                    └────────────────┘
```

---

## Backend Architecture

### Service Layer Design

```
┌─────────────────────────────────────────────────────────────┐
│                     Flask Application                        │
├─────────────────────────────────────────────────────────────┤
│                                                               │
│  ┌────────────────────────────────────────────────────┐    │
│  │              routes/                                │    │
│  │                                                      │    │
│  │  api_routes.py                                      │    │
│  │  ├── POST /api/analyze                              │    │
│  │  ├── GET  /api/health                               │    │
│  │  └── GET  /api/skills/categories                    │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │              services/                              │    │
│  │                                                      │    │
│  │  file_processor.py                                  │    │
│  │  ├── validate_file(file) -> bool                   │    │
│  │  ├── extract_text_pdf(file) -> str                 │    │
│  │  └── extract_text_docx(file) -> str                │    │
│  │                                                      │    │
│  │  nlp_service.py                                     │    │
│  │  ├── extract_skills(text) -> List[Skill]           │    │
│  │  ├── extract_experience(text) -> List[Experience]  │    │
│  │  ├── calculate_score(data) -> float                │    │
│  │  └── categorize_skills(skills) -> Dict             │    │
│  │                                                      │    │
│  │  ai_service.py                                      │    │
│  │  ├── generate_suggestions(resume_data) -> List     │    │
│  │  ├── analyze_content_quality(text) -> Dict         │    │
│  │  └── get_ats_recommendations(text) -> List         │    │
│  │                                                      │    │
│  │  analyzer.py                                        │    │
│  │  └── analyze_resume(file) -> AnalysisResult        │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │              models/                                │    │
│  │                                                      │    │
│  │  resume.py        - Resume data model               │    │
│  │  skill.py         - Skill model                     │    │
│  │  experience.py    - Experience model                │    │
│  │  analysis.py      - Analysis result model           │    │
│  └────────────────────────────────────────────────────┘    │
│                          │                                   │
│  ┌────────────────────────────────────────────────────┐    │
│  │              utils/                                 │    │
│  │                                                      │    │
│  │  validators.py    - Input validation               │    │
│  │  constants.py     - App constants                  │    │
│  │  exceptions.py    - Custom exceptions              │    │
│  └────────────────────────────────────────────────────┘    │
│                                                               │
└─────────────────────────────────────────────────────────────┘
```

### Module Responsibilities

**File Processor Service**
- Validates file type and size
- Extracts text from PDF using pdfplumber and PyPDF2 (fallback)
- Extracts text from DOCX using python-docx
- Handles encoding issues
- Returns structured text data

**NLP Service**
- Loads spaCy and BERT models
- Identifies technical and soft skills
- Extracts entities (companies, job titles, dates)
- Parses experience timeline
- Calculates resume score based on multiple factors

**AI Service**
- Interfaces with OpenAI GPT-4 API
- Generates personalized improvement suggestions
- Analyzes content quality (action verbs, quantification, clarity)
- Provides ATS optimization recommendations
- Implements retry logic and error handling

**Analyzer (Orchestrator)**
- Coordinates all services
- Manages async processing
- Combines results from all services
- Handles errors and fallbacks
- Returns unified analysis result

---

## API Structure

### Endpoints

#### 1. POST /api/analyze

**Purpose**: Upload and analyze a resume

**Request**:
```http
POST /api/analyze HTTP/1.1
Content-Type: multipart/form-data

file: <binary-data>
```

**Response** (200 OK):
```json
{
  "success": true,
  "data": {
    "overall_score": 85,
    "skills": {
      "technical": [
        {"name": "Python", "proficiency": "advanced", "count": 5},
        {"name": "JavaScript", "proficiency": "intermediate", "count": 3}
      ],
      "soft": [
        {"name": "Leadership", "count": 4},
        {"name": "Communication", "count": 3}
      ],
      "categories": {
        "programming_languages": ["Python", "JavaScript", "Java"],
        "frameworks": ["React", "Flask", "Django"],
        "tools": ["Git", "Docker", "AWS"]
      }
    },
    "experience": [
      {
        "title": "Senior Software Engineer",
        "company": "Tech Corp",
        "start_date": "2020-01",
        "end_date": "2023-12",
        "duration_months": 48,
        "responsibilities": [
          "Led team of 5 developers",
          "Architected microservices platform"
        ]
      }
    ],
    "education": [
      {
        "degree": "Bachelor of Science",
        "field": "Computer Science",
        "institution": "University Name",
        "year": 2019
      }
    ],
    "ai_suggestions": [
      {
        "category": "content",
        "priority": "high",
        "suggestion": "Add quantifiable metrics to your achievements",
        "examples": [
          "Instead of 'Improved performance', write 'Improved performance by 40%'"
        ]
      },
      {
        "category": "formatting",
        "priority": "medium",
        "suggestion": "Use consistent date formatting throughout"
      }
    ],
    "ats_score": 78,
    "ats_recommendations": [
      "Add more industry-specific keywords",
      "Ensure consistent formatting for dates"
    ],
    "analysis": {
      "total_experience_years": 4,
      "action_verb_usage": 0.65,
      "quantification_rate": 0.45,
      "keyword_density": 0.12
    }
  },
  "processing_time": 2.4
}
```

**Error Responses**:

400 Bad Request:
```json
{
  "success": false,
  "error": {
    "code": "INVALID_FILE_TYPE",
    "message": "Only PDF and DOCX files are supported",
    "details": {
      "allowed_types": ["application/pdf", "application/vnd.openxmlformats-officedocument.wordprocessingml.document"]
    }
  }
}
```

413 Payload Too Large:
```json
{
  "success": false,
  "error": {
    "code": "FILE_TOO_LARGE",
    "message": "File size exceeds 5MB limit",
    "details": {
      "max_size_mb": 5,
      "received_size_mb": 7.2
    }
  }
}
```

429 Too Many Requests:
```json
{
  "success": false,
  "error": {
    "code": "RATE_LIMIT_EXCEEDED",
    "message": "Too many requests. Please try again later.",
    "details": {
      "retry_after": 60
    }
  }
}
```

#### 2. GET /api/health

**Purpose**: Health check endpoint

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-10-21T10:30:00Z",
  "services": {
    "nlp": "ready",
    "ai": "ready",
    "file_processor": "ready"
  },
  "version": "1.0.0"
}
```

#### 3. GET /api/skills/categories

**Purpose**: Get list of supported skill categories

**Response** (200 OK):
```json
{
  "categories": [
    {
      "name": "programming_languages",
      "display_name": "Programming Languages",
      "example_skills": ["Python", "JavaScript", "Java", "C++"]
    },
    {
      "name": "frameworks",
      "display_name": "Frameworks & Libraries",
      "example_skills": ["React", "Django", "TensorFlow"]
    }
  ]
}
```

---

## Data Flow

### Resume Analysis Flow

```
┌─────────┐
│  User   │
└────┬────┘
     │ 1. Upload resume file (PDF/DOCX)
     ▼
┌─────────────────┐
│  Frontend       │
│  Validation     │
│  • File type    │
│  • File size    │
└────┬────────────┘
     │ 2. POST /api/analyze
     ▼
┌─────────────────┐
│  API Gateway    │
│  • Rate limit   │
│  • CORS check   │
└────┬────────────┘
     │ 3. Pass to analyzer
     ▼
┌──────────────────────────────────────────────┐
│           Analyzer (Orchestrator)            │
└──────────────────┬───────────────────────────┘
                   │
     ┌─────────────┼─────────────┐
     │             │             │
     ▼             ▼             ▼
┌─────────┐  ┌─────────┐  ┌──────────┐
│  File   │  │   NLP   │  │    AI    │
│ Process │  │ Service │  │ Service  │
└────┬────┘  └────┬────┘  └────┬─────┘
     │            │            │
     │ 4. Extract │ 5. Analyze │ 6. Generate
     │    text    │    content │    suggestions
     │            │            │
     ▼            ▼            ▼
┌────────────────────────────────┐
│      Text Extraction           │
│      "Experienced developer    │
│       with Python..."          │
└────────────┬───────────────────┘
             │
             ▼
┌────────────────────────────────┐
│      NLP Processing            │
│                                │
│  spaCy Pipeline:               │
│  ├── Tokenization              │
│  ├── POS Tagging               │
│  ├── NER                       │
│  └── Dependency Parsing        │
│                                │
│  Skill Extraction:             │
│  ├── Pattern matching          │
│  ├── Entity recognition        │
│  └── Categorization            │
│                                │
│  Experience Parsing:           │
│  ├── Date extraction           │
│  ├── Job title identification  │
│  └── Company recognition       │
└────────────┬───────────────────┘
             │
             ▼
┌────────────────────────────────┐
│      AI Analysis (GPT-4)       │
│                                │
│  Prompt Engineering:           │
│  ┌──────────────────────────┐ │
│  │ System: You are a        │ │
│  │ professional resume      │ │
│  │ reviewer...              │ │
│  │                          │ │
│  │ User: Analyze this       │ │
│  │ resume and provide       │ │
│  │ suggestions...           │ │
│  └──────────────────────────┘ │
│                                │
│  Response Processing:          │
│  ├── Parse suggestions         │
│  ├── Categorize feedback       │
│  └── Prioritize recommendations│
└────────────┬───────────────────┘
             │
             ▼
┌────────────────────────────────┐
│    Combine & Score             │
│                                │
│  Score Calculation:            │
│  ├── Skills diversity (30%)    │
│  ├── Experience depth (25%)    │
│  ├── Content quality (25%)     │
│  ├── ATS optimization (20%)    │
│  └── Overall = weighted avg    │
└────────────┬───────────────────┘
             │
             ▼
┌────────────────────────────────┐
│    Build JSON Response         │
│    {                           │
│      overall_score: 85,        │
│      skills: {...},            │
│      experience: [...],        │
│      ai_suggestions: [...]     │
│    }                           │
└────────────┬───────────────────┘
             │ 7. Return results
             ▼
┌────────────────────────────────┐
│    Frontend Results Display    │
│    • Score visualization       │
│    • Skills breakdown          │
│    • Timeline chart            │
│    • Improvement checklist     │
└────────────────────────────────┘
```

### Error Handling Flow

```
┌──────────────┐
│ Error Occurs │
└──────┬───────┘
       │
       ▼
┌──────────────────────┐
│ Error Type Check     │
└──────┬───────────────┘
       │
       ├─── Validation Error (400)
       │    └──▶ Return field-specific error messages
       │
       ├─── File Processing Error (422)
       │    └──▶ Return parsing failure details
       │
       ├─── Rate Limit Error (429)
       │    └──▶ Return retry-after header
       │
       ├─── Server Error (500)
       │    ├──▶ Log full stack trace
       │    └──▶ Return generic error to user
       │
       └─── External API Error (503)
            ├──▶ Retry with exponential backoff
            └──▶ Return service unavailable
```

---

## Component Interactions

### Sequence Diagram: Complete Analysis Flow

```
User      Frontend    API       Analyzer   FileProc   NLP       AI        Response
 │           │         │           │          │         │         │           │
 │  Upload   │         │           │          │         │         │           │
 ├──────────▶│         │           │          │         │         │           │
 │           │ Validate│           │          │         │         │           │
 │           ├────┐    │           │          │         │         │           │
 │           │    │    │           │          │         │         │           │
 │           │◀───┘    │           │          │         │         │           │
 │           │  POST   │           │          │         │         │           │
 │           ├────────▶│           │          │         │         │           │
 │           │         │ Rate Check│          │         │         │           │
 │           │         ├──────┐    │          │         │         │           │
 │           │         │      │    │          │         │         │           │
 │           │         │◀─────┘    │          │         │         │           │
 │           │         │  Analyze  │          │         │         │           │
 │           │         ├──────────▶│          │         │         │           │
 │           │         │           │ Extract  │         │         │           │
 │           │         │           ├─────────▶│         │         │           │
 │           │         │           │   Text   │         │         │           │
 │           │         │           │◀─────────┤         │         │           │
 │           │         │           │          │         │         │           │
 │           │         │           │ Parse Skills       │         │           │
 │           │         │           ├────────────────────▶         │           │
 │           │         │           │          Skills    │         │           │
 │           │         │           │◀────────────────────┤         │           │
 │           │         │           │                     │         │           │
 │           │         │           │ Parse Experience    │         │           │
 │           │         │           ├────────────────────▶│         │           │
 │           │         │           │      Experience     │         │           │
 │           │         │           │◀────────────────────┤         │           │
 │           │         │           │                     │         │           │
 │           │         │           │ Generate Suggestions│         │           │
 │           │         │           ├────────────────────────────────▶          │
 │           │         │           │              Suggestions       │           │
 │           │         │           │◀────────────────────────────────┤          │
 │           │         │           │                     │         │           │
 │           │         │           │ Build Result                   │           │
 │           │         │           ├────────────────────────────────────────────▶
 │           │         │           │                     │         │      JSON  │
 │           │         │  Result   │◀────────────────────────────────────────────┤
 │           │         │◀──────────┤                     │         │           │
 │           │  JSON   │           │                     │         │           │
 │           │◀────────┤           │                     │         │           │
 │  Display  │         │           │                     │         │           │
 │◀──────────┤         │           │                     │         │           │
 │           │         │           │                     │         │           │
```

---

## Database Schema

### Phase 1 (No Database - In-Memory Processing)

In Phase 1, we don't persist data. All processing is stateless.

### Phase 2 (Optional: User Accounts & History)

```sql
-- Users table
CREATE TABLE users (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    last_login TIMESTAMP
);

-- Resume analyses table
CREATE TABLE analyses (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID REFERENCES users(id) ON DELETE CASCADE,
    filename VARCHAR(255) NOT NULL,
    file_hash VARCHAR(64) NOT NULL, -- SHA-256 hash
    overall_score DECIMAL(5,2),
    ats_score DECIMAL(5,2),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP, -- Auto-delete after 24 hours
    analysis_data JSONB -- Store full analysis result
);

-- Skills extracted (for analytics)
CREATE TABLE extracted_skills (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    analysis_id UUID REFERENCES analyses(id) ON DELETE CASCADE,
    skill_name VARCHAR(100) NOT NULL,
    category VARCHAR(50),
    proficiency VARCHAR(20),
    count INTEGER DEFAULT 1
);

-- Indexes for performance
CREATE INDEX idx_analyses_user_id ON analyses(user_id);
CREATE INDEX idx_analyses_created_at ON analyses(created_at);
CREATE INDEX idx_skills_analysis_id ON extracted_skills(analysis_id);
CREATE INDEX idx_skills_name ON extracted_skills(skill_name);
```

---

## Technology Stack Justification

### Why Flask?
- **Lightweight**: No unnecessary overhead
- **Flexible**: Easy to structure as needed
- **Python Ecosystem**: Direct access to ML/NLP libraries
- **Async Support**: Can handle long-running tasks
- **Easy Testing**: Simple to write unit and integration tests

### Why React?
- **Component Reusability**: Build once, use everywhere
- **Rich Ecosystem**: Tons of libraries and tools
- **Performance**: Virtual DOM for fast updates
- **Developer Experience**: Hot reload, debugging tools
- **Community**: Large community, lots of resources

### Why spaCy over NLTK?
- **Speed**: 10x faster than NLTK for NER
- **Accuracy**: Pre-trained models with 90%+ accuracy
- **Production-Ready**: Designed for real-world applications
- **Modern Architecture**: Uses neural networks

### Why GPT-4 for Suggestions?
- **Contextual Understanding**: Understands nuances
- **Natural Language**: Generates human-like suggestions
- **Customizable**: Fine-tune with prompts
- **Proven**: Industry-standard for text generation

---

## Performance Considerations

### Optimization Strategies

1. **Caching**
   - Cache skill categories (Redis)
   - Cache common resume patterns
   - Cache AI responses for similar resumes

2. **Async Processing**
   - Process NLP and AI in parallel
   - Use Celery for background jobs (Phase 2)

3. **Resource Management**
   - Limit concurrent analyses
   - Auto-cleanup uploaded files
   - Connection pooling for external APIs

4. **Frontend Optimization**
   - Code splitting
   - Lazy loading components
   - Compress API responses (gzip)

### Expected Performance

| Metric | Target | Acceptable |
|--------|--------|------------|
| API Response Time | <2s | <5s |
| File Upload Time | <1s | <3s |
| NLP Processing | <3s | <8s |
| AI Suggestions | <5s | <10s |
| Total Analysis | <10s | <20s |

---

## Security Architecture

```
┌─────────────────────────────────────────────┐
│          Security Layers                     │
├─────────────────────────────────────────────┤
│                                              │
│  1. Frontend Validation                     │
│     ├── File type check                     │
│     ├── File size check                     │
│     └── Sanitize inputs                     │
│                                              │
│  2. API Gateway Security                    │
│     ├── Rate limiting (10 req/min)          │
│     ├── CORS validation                     │
│     ├── Request size limits                 │
│     └── Content-Type validation             │
│                                              │
│  3. Backend Validation                      │
│     ├── Magic byte file type check          │
│     ├── Input sanitization                  │
│     ├── Schema validation (Marshmallow)     │
│     └── Path traversal prevention           │
│                                              │
│  4. Data Protection                         │
│     ├── No PII logging                      │
│     ├── Secure temp file handling           │
│     ├── Auto-deletion (24h)                 │
│     └── Encrypted API keys (env vars)       │
│                                              │
│  5. External API Security                   │
│     ├── API key rotation                    │
│     ├── Request signing                     │
│     ├── Timeout configuration               │
│     └── Error message sanitization          │
│                                              │
└─────────────────────────────────────────────┘
```

---

## Scalability Plan

### Phase 1: Single Server
- Handle 100 concurrent users
- Vertical scaling (more CPU/RAM)

### Phase 2: Load Balanced
```
       ┌─────────────┐
       │Load Balancer│
       └──────┬──────┘
              │
    ┌─────────┼─────────┐
    ▼         ▼         ▼
┌────────┐┌────────┐┌────────┐
│ App 1  ││ App 2  ││ App 3  │
└────────┘└────────┘└────────┘
    │         │         │
    └─────────┼─────────┘
              ▼
       ┌─────────────┐
       │   Redis     │
       │   Cache     │
       └─────────────┘
```

### Phase 3: Microservices
- Separate NLP service
- Separate AI service
- Message queue (RabbitMQ)
- Distributed caching

---

This architecture provides a solid foundation for the Resume Analyzer, balancing simplicity for Phase 1 MVP with clear paths for future scaling and enhancements.
