# Language Translation API

[![CI/CD Pipeline](https://github.com/yourusername/language-translation-api/actions/workflows/ci.yml/badge.svg)](https://github.com/yourusername/language-translation-api/actions/workflows/ci.yml)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.104.1-009688.svg)](https://fastapi.tiangolo.com)
[![Code Coverage](https://img.shields.io/badge/coverage-%3E75%25-brightgreen.svg)](https://github.com/yourusername/language-translation-api)

A robust and scalable REST API for translating text between multiple languages, built with FastAPI and following DevOps best practices.

## 📋 Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Running the Application](#running-the-application)
- [Running Tests](#running-tests)
- [CI/CD Pipeline](#cicd-pipeline)
- [Docker Support](#docker-support)
- [API Documentation](#api-documentation)
- [Development](#development)

## ✨ Features

- **FastAPI Framework**: High-performance async API
- **Comprehensive Testing**: Unit, integration, and system tests with pytest
- **Code Coverage**: Enforced minimum 75% coverage
- **Code Quality**: Pylint linting with minimum score of 7.5/10
- **Security Scanning**: Bandit security checks for vulnerabilities
- **CI/CD Pipeline**: Automated GitHub Actions workflow
- **Docker Support**: Containerized deployment
- **Health Check Endpoint**: Built-in monitoring endpoint

## 📁 Project Structure

```
language-translation-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py                    # FastAPI application entry point
│   ├── api/
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── routes.py          # API routes (placeholder)
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py              # Configuration management
│   ├── services/
│   │   ├── __init__.py
│   │   └── translator.py          # Translation service (placeholder)
│   ├── models/
│   │   ├── __init__.py
│   │   └── db.py                  # Database models (placeholder)
│   └── tests/
│       ├── unit/                  # Unit tests
│       ├── integration/           # Integration tests
│       └── system/                # System tests
│
├── .github/
│   └── workflows/
│       └── ci.yml                 # CI/CD pipeline configuration
│
├── scripts/
│   └── create_artifact.sh         # Deployment package creation script
│
├── .env.example                   # Environment variables template
├── .gitignore                     # Git ignore rules
├── .pylintrc                      # Pylint configuration
├── docker-compose.yml             # Docker Compose configuration
├── Dockerfile                     # Docker image definition
├── pytest.ini                     # Pytest configuration
├── README.md                      # This file
├── requirements.txt               # Python dependencies
└── postman_collection.json        # API testing collection (placeholder)
```

## 🔧 Prerequisites

- Python 3.10 or higher
- pip (Python package manager)
- Docker (optional, for containerized deployment)
- Git

## 📦 Installation

1. **Clone the repository**

```bash
git clone https://github.com/yourusername/language-translation-api.git
cd language-translation-api
```

2. **Create a virtual environment**

```bash
python -m venv venv

# On Windows
venv\Scripts\activate

# On Linux/Mac
source venv/bin/activate
```

3. **Install dependencies**

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

4. **Set up environment variables**

```bash
# Copy the example environment file
cp .env.example .env

# Edit .env with your actual configuration
```

## 🚀 Running the Application

### Local Development

```bash
# Run with uvicorn directly
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Or run the main module
python -m app.main
```

The API will be available at:
- **API**: http://localhost:8000
- **Health Check**: http://localhost:8000/health
- **Interactive Docs**: http://localhost:8000/docs
- **Alternative Docs**: http://localhost:8000/redoc

### Using Docker

```bash
# Build the Docker image
docker build -t translation-api .

# Run the container
docker run -p 8000:8000 translation-api

# Or use Docker Compose
docker-compose up --build
```

## 🧪 Running Tests

### Run All Tests

```bash
pytest app/tests/ -v
```

### Run Specific Test Categories

```bash
# Unit tests only
pytest app/tests/unit/ -v

# Integration tests only
pytest app/tests/integration/ -v

# System tests only
pytest app/tests/system/ -v
```

### Run Tests with Coverage

```bash
# Generate coverage report
pytest app/tests/ --cov=app --cov-report=html --cov-report=term-missing

# View HTML coverage report
# Open htmlcov/index.html in your browser
```

### Run Linting

```bash
# Run pylint
pylint app/ --rcfile=.pylintrc
```

### Run Security Scan

```bash
# Run bandit security scan
bandit -r app/ -f txt
```

## 🔄 CI/CD Pipeline

The project includes a comprehensive GitHub Actions CI/CD pipeline that runs on every push and pull request.

### Pipeline Stages

1. **Build**: Install dependencies and verify syntax
2. **Test**: Run all tests with pytest
3. **Coverage**: Ensure code coverage ≥ 75%
4. **Lint**: Check code quality with pylint (score ≥ 7.5)
5. **Security**: Scan for vulnerabilities with bandit
6. **Deploy**: Create deployment package with reports

### Pipeline Triggers

- Push to `main`, `dev`, or `feature/*` branches
- Pull requests to `main`, `dev`, or `feature/*` branches

### Artifacts

The pipeline generates the following artifacts:
- Coverage reports (HTML, XML, text)
- Pylint report
- Bandit security report
- Deployment package (zip file with code and reports)

## 🐳 Docker Support

### Dockerfile

The project includes a production-ready Dockerfile with:
- Python 3.10 slim base image
- Non-root user for security
- Health check configuration
- Optimized layer caching

### Docker Compose

Use Docker Compose for easy local development:

```bash
# Start all services
docker-compose up

# Start in detached mode
docker-compose up -d

# View logs
docker-compose logs -f

# Stop services
docker-compose down
```

## 📚 API Documentation

### Available Endpoints

#### Health Check
```
GET /health
```
Returns the API health status.

**Response:**
```json
{
  "status": "ok"
}
```

#### Root
```
GET /
```
Returns API information and available endpoints.

**Response:**
```json
{
  "message": "Welcome to Language Translation API",
  "version": "1.0.0",
  "endpoints": {
    "health": "/health",
    "docs": "/docs"
  }
}
```

### Interactive Documentation

FastAPI automatically generates interactive API documentation:
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

## 👨‍💻 Development

### Code Quality Standards

- **Minimum Test Coverage**: 75%
- **Minimum Pylint Score**: 7.5/10
- **Security**: No HIGH severity issues allowed
- **Code Style**: Follow PEP 8 guidelines
- **Documentation**: Docstrings for all public functions/classes

### Adding New Features

1. Create a feature branch
```bash
git checkout -b feature/your-feature-name
```

2. Implement your feature with tests
3. Ensure all tests pass and coverage meets threshold
4. Commit and push your changes
5. Create a pull request

### Running Quality Checks Locally

Before committing, run these checks:

```bash
# Run tests
pytest app/tests/ -v

# Check coverage
pytest app/tests/ --cov=app --cov-report=term-missing --cov-fail-under=75

# Run linting
pylint app/ --rcfile=.pylintrc

# Run security scan
bandit -r app/
```

### Creating Deployment Package

```bash
# Make script executable (Linux/Mac)
chmod +x scripts/create_artifact.sh

# Run the script
./scripts/create_artifact.sh
```

## 📝 Environment Variables

The following environment variables can be configured:

| Variable | Description | Default |
|----------|-------------|---------|
| `API_KEY` | API key for translation service | - |
| `DATABASE_URL` | Database connection string | - |
| `LOG_ENCRYPT_KEY` | Encryption key for logs | - |
| `ENVIRONMENT` | Application environment | `development` |
| `HOST` | Server host | `0.0.0.0` |
| `PORT` | Server port | `8000` |
| `LOG_LEVEL` | Logging level | `INFO` |

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes with tests
4. Ensure all quality checks pass
5. Submit a pull request

## 📄 License

This project is part of a DevOps learning initiative.

## 🆘 Support

For issues and questions:
- Create an issue on GitHub
- Check the documentation at `/docs`
- Review the CI/CD pipeline logs

## 🎯 Next Steps

This is a Sprint 1-2 skeleton setup. Future sprints will include:
- Translation service implementation
- Database integration
- Caching layer
- Rate limiting
- Authentication/Authorization
- Advanced logging and monitoring
- Performance optimization

---

**Built with ❤️ using FastAPI and DevOps best practices**
