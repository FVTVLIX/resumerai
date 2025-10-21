# Deployment Guide

## Table of Contents
1. [Prerequisites](#prerequisites)
2. [Environment Setup](#environment-setup)
3. [Heroku Deployment](#heroku-deployment)
4. [AWS Deployment](#aws-deployment)
5. [Docker Deployment](#docker-deployment)
6. [Frontend Deployment (Vercel/Netlify)](#frontend-deployment)
7. [Production Checklist](#production-checklist)

---

## Prerequisites

- Git repository
- OpenAI API key
- Cloud platform account (Heroku, AWS, etc.)
- Domain name (optional)

---

## Environment Setup

### Required Environment Variables

**Backend (.env)**
```bash
FLASK_ENV=production
SECRET_KEY=<generate-strong-secret-key>
DEBUG=False

OPENAI_API_KEY=<your-openai-api-key>
OPENAI_MODEL=gpt-4
ENABLE_AI_SUGGESTIONS=True

SPACY_MODEL=en_core_web_lg

CORS_ORIGINS=https://your-frontend-domain.com
PORT=5000

# For production with Redis
REDIS_URL=redis://your-redis-url:6379
```

**Frontend (.env.production)**
```bash
VITE_API_URL=https://your-backend-api.com/api
```

---

## Heroku Deployment

### Backend Deployment on Heroku

#### 1. Install Heroku CLI

```bash
# macOS
brew tap heroku/brew && brew install heroku

# Windows
# Download from https://devcenter.heroku.com/articles/heroku-cli

# Linux
curl https://cli-assets.heroku.com/install.sh | sh
```

#### 2. Prepare Backend for Heroku

Create **`backend/Procfile`**:
```
web: gunicorn app:app
```

Create **`backend/runtime.txt`**:
```
python-3.11.0
```

Update **`backend/requirements.txt`** to include:
```
gunicorn==21.2.0
```

#### 3. Deploy Backend

```bash
cd backend

# Login to Heroku
heroku login

# Create new app
heroku create resume-analyzer-api

# Set environment variables
heroku config:set FLASK_ENV=production
heroku config:set SECRET_KEY=$(openssl rand -hex 32)
heroku config:set OPENAI_API_KEY=your-openai-key
heroku config:set SPACY_MODEL=en_core_web_lg
heroku config:set CORS_ORIGINS=https://your-frontend.vercel.app

# Add buildpacks for spaCy
heroku buildpacks:add heroku/python

# Create Procfile to download spaCy model
# Add to Procfile:
# release: python -m spacy download en_core_web_lg

# Add Redis addon (for rate limiting)
heroku addons:create heroku-redis:mini

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Scale dynos
heroku ps:scale web=1

# Open app
heroku open

# View logs
heroku logs --tail
```

#### 4. Configure spaCy Model Download

Add to **`backend/Procfile`**:
```
release: python -m spacy download en_core_web_lg
web: gunicorn app:app
```

Or create a **`backend/download_models.py`**:
```python
import spacy

spacy.cli.download("en_core_web_lg")
```

And update Procfile:
```
release: python download_models.py
web: gunicorn app:app
```

---

## AWS Deployment

### Backend on AWS Elastic Beanstalk

#### 1. Install EB CLI

```bash
pip install awsebcli
```

#### 2. Initialize EB Application

```bash
cd backend

eb init -p python-3.11 resume-analyzer

# Create environment
eb create resume-analyzer-env

# Set environment variables
eb setenv FLASK_ENV=production \
          SECRET_KEY=$(openssl rand -hex 32) \
          OPENAI_API_KEY=your-key \
          SPACY_MODEL=en_core_web_lg

# Deploy
eb deploy

# Open app
eb open

# Check status
eb status

# View logs
eb logs
```

#### 3. Configure for spaCy

Create **`.ebextensions/01_packages.config`**:
```yaml
commands:
  01_download_spacy_model:
    command: "source /var/app/venv/*/bin/activate && python -m spacy download en_core_web_lg"
```

### Backend on AWS Lambda (Serverless)

Use **Zappa** for serverless deployment:

```bash
pip install zappa

# Initialize Zappa
zappa init

# Deploy
zappa deploy production

# Update
zappa update production
```

---

## Docker Deployment

### Backend Dockerfile

Create **`backend/Dockerfile`**:
```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Download spaCy model
RUN python -m spacy download en_core_web_lg

# Copy application code
COPY . .

# Expose port
EXPOSE 5000

# Run application
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--timeout", "120", "app:app"]
```

### Frontend Dockerfile

Create **`frontend/Dockerfile`**:
```dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci

# Copy source code
COPY . .

# Build application
RUN npm run build

# Production stage
FROM nginx:alpine

# Copy built files
COPY --from=build /app/dist /usr/share/nginx/html

# Copy nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]
```

Create **`frontend/nginx.conf`**:
```nginx
server {
    listen 80;
    server_name _;

    root /usr/share/nginx/html;
    index index.html;

    location / {
        try_files $uri $uri/ /index.html;
    }

    location /api {
        proxy_pass http://backend:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### Docker Compose

Create **`docker-compose.yml`** at project root:
```yaml
version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "5000:5000"
    environment:
      - FLASK_ENV=production
      - SECRET_KEY=${SECRET_KEY}
      - OPENAI_API_KEY=${OPENAI_API_KEY}
      - REDIS_URL=redis://redis:6379
    depends_on:
      - redis
    volumes:
      - ./backend:/app
    networks:
      - app-network

  frontend:
    build: ./frontend
    ports:
      - "80:80"
    depends_on:
      - backend
    networks:
      - app-network

  redis:
    image: redis:alpine
    ports:
      - "6379:6379"
    networks:
      - app-network

networks:
  app-network:
    driver: bridge
```

### Deploy with Docker Compose

```bash
# Build and start services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down

# Rebuild and restart
docker-compose up -d --build
```

---

## Frontend Deployment

### Deploy to Vercel

```bash
cd frontend

# Install Vercel CLI
npm install -g vercel

# Deploy
vercel

# Set environment variables
vercel env add VITE_API_URL production
# Enter your backend API URL when prompted

# Deploy to production
vercel --prod
```

### Deploy to Netlify

```bash
cd frontend

# Install Netlify CLI
npm install -g netlify-cli

# Build
npm run build

# Deploy
netlify deploy

# Deploy to production
netlify deploy --prod
```

Create **`frontend/netlify.toml`**:
```toml
[build]
  command = "npm run build"
  publish = "dist"

[[redirects]]
  from = "/*"
  to = "/index.html"
  status = 200

[build.environment]
  VITE_API_URL = "https://your-backend-api.herokuapp.com/api"
```

### Deploy to AWS S3 + CloudFront

```bash
cd frontend

# Build
npm run build

# Install AWS CLI
# Upload to S3
aws s3 sync dist/ s3://your-bucket-name --delete

# Invalidate CloudFront cache
aws cloudfront create-invalidation --distribution-id YOUR_DIST_ID --paths "/*"
```

---

## Production Checklist

### Security

- [ ] Set strong SECRET_KEY
- [ ] Enable HTTPS/SSL
- [ ] Configure CORS properly
- [ ] Implement rate limiting
- [ ] Sanitize all inputs
- [ ] Set secure headers
- [ ] Use environment variables for secrets
- [ ] Enable authentication (Phase 2)

### Performance

- [ ] Enable gzip compression
- [ ] Configure CDN (CloudFront, Cloudflare)
- [ ] Optimize images
- [ ] Enable browser caching
- [ ] Use production builds
- [ ] Monitor API response times
- [ ] Set up database connection pooling (if using DB)

### Monitoring

- [ ] Set up error tracking (Sentry)
- [ ] Configure logging
- [ ] Set up uptime monitoring
- [ ] Create health check endpoints
- [ ] Monitor API rate limits
- [ ] Track OpenAI API usage

### Backup & Recovery

- [ ] Back up environment variables
- [ ] Document deployment process
- [ ] Create rollback plan
- [ ] Test disaster recovery

---

## Environment-Specific Configurations

### Development

```bash
FLASK_ENV=development
DEBUG=True
ENABLE_AI_SUGGESTIONS=False  # Save API costs
```

### Staging

```bash
FLASK_ENV=production
DEBUG=False
ENABLE_AI_SUGGESTIONS=True
LOG_LEVEL=INFO
```

### Production

```bash
FLASK_ENV=production
DEBUG=False
ENABLE_AI_SUGGESTIONS=True
LOG_LEVEL=WARNING
SENTRY_DSN=your-sentry-dsn
```

---

## Scaling Considerations

### Horizontal Scaling

```bash
# Heroku
heroku ps:scale web=3

# AWS EB
eb scale 3

# Docker Compose
docker-compose up -d --scale backend=3
```

### Vertical Scaling

```bash
# Heroku (upgrade dyno)
heroku ps:resize web=performance-m

# AWS EB (change instance type)
eb scale --instance-type t3.medium
```

### Caching

- Implement Redis for session/cache storage
- Cache spaCy NLP results
- Cache skill categories

---

## CI/CD Setup

### GitHub Actions

Create **`.github/workflows/deploy.yml`**:
```yaml
name: Deploy

on:
  push:
    branches: [main]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Run tests
        run: |
          cd backend
          pip install -r requirements.txt
          pytest

  deploy-backend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - uses: akhileshns/heroku-deploy@v3.12.12
        with:
          heroku_api_key: ${{secrets.HEROKU_API_KEY}}
          heroku_app_name: "resume-analyzer-api"
          heroku_email: "your-email@example.com"

  deploy-frontend:
    needs: test
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Vercel
        uses: amondnet/vercel-action@v20
        with:
          vercel-token: ${{ secrets.VERCEL_TOKEN }}
          vercel-org-id: ${{ secrets.ORG_ID}}
          vercel-project-id: ${{ secrets.PROJECT_ID}}
```

---

## Troubleshooting

### Common Issues

1. **spaCy model not found**
   - Ensure model is downloaded in release/build phase
   - Check disk space
   - Verify model name in config

2. **OpenAI API errors**
   - Check API key is set
   - Verify API quota/limits
   - Check network connectivity

3. **CORS errors**
   - Verify frontend URL in CORS_ORIGINS
   - Check protocol (http vs https)

4. **File upload failures**
   - Check file size limits
   - Verify temp directory permissions
   - Check disk space

---

This deployment guide covers multiple platforms and scenarios. Choose the one that best fits your needs and budget.
