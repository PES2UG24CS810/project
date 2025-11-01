# Quick Setup Guide for Language Translation API

## 🚀 Quick Start (Windows)

### 1. Setup Python Environment

```powershell
# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

### 2. Configure Environment

```powershell
# Copy example environment file
copy .env.example .env

# Edit .env file with your configuration (optional for local testing)
```

### 3. Run the Application

```powershell
# Start the FastAPI server
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- http://localhost:8000
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs

### 4. Run Tests

```powershell
# Run all tests
pytest app/tests/ -v

# Run with coverage
pytest app/tests/ --cov=app --cov-report=html --cov-report=term-missing
```

### 5. Run Quality Checks

```powershell
# Pylint (code quality)
pylint app/ --rcfile=.pylintrc

# Bandit (security scan)
bandit -r app/ -f txt
```

### 6. Docker Build (Optional)

```powershell
# Build image
docker build -t translation-api .

# Run container
docker run -p 8000:8000 translation-api

# Or use Docker Compose
docker-compose up --build
```

## 🧪 Testing the API

### Using cURL (PowerShell)

```powershell
# Health check
Invoke-WebRequest -Uri http://localhost:8000/health | Select-Object -ExpandProperty Content

# Root endpoint
Invoke-WebRequest -Uri http://localhost:8000/ | Select-Object -ExpandProperty Content
```

### Using Browser
Simply open:
- http://localhost:8000/health
- http://localhost:8000/docs (Interactive API documentation)

## 📊 CI/CD Pipeline

The GitHub Actions pipeline automatically runs on push/PR to:
- `main`
- `dev`
- `feature/**` branches

Pipeline stages:
1. ✅ Build - Install dependencies and check syntax
2. ✅ Test - Run all tests
3. ✅ Coverage - Ensure ≥75% coverage
4. ✅ Lint - Check code quality (≥7.5/10)
5. ✅ Security - Scan with Bandit (no HIGH severity)
6. ✅ Deploy - Create deployment package

## 📦 Project Files Overview

### Core Application Files
- `app/main.py` - FastAPI application with health check endpoint
- `app/core/config.py` - Configuration management
- `app/services/translator.py` - Translation service placeholder
- `app/models/db.py` - Database models placeholder
- `app/api/v1/routes.py` - API routes placeholder

### Configuration Files
- `requirements.txt` - Python dependencies
- `pytest.ini` - Pytest configuration
- `.pylintrc` - Pylint configuration
- `.env.example` - Environment variables template
- `Dockerfile` - Docker image definition
- `docker-compose.yml` - Docker Compose configuration

### CI/CD Files
- `.github/workflows/ci.yml` - Complete CI/CD pipeline
- `scripts/create_artifact.sh` - Deployment package creation

### Documentation
- `README.md` - Comprehensive documentation
- `postman_collection.json` - API testing collection

## 🎯 Next Steps

1. Install dependencies: `pip install -r requirements.txt`
2. Run tests: `pytest app/tests/ -v`
3. Start server: `uvicorn app.main:app --reload`
4. Open docs: http://localhost:8000/docs
5. Push to GitHub to trigger CI/CD pipeline

## 💡 Tips

- Always activate virtual environment before running commands
- Run tests before committing code
- Check coverage: `pytest --cov=app --cov-report=term-missing`
- Use `--reload` flag during development for auto-reload
- View detailed API docs at `/docs` endpoint

---

For detailed documentation, see `README.md`
