#!/bin/bash
# Script to create deployment artifact package
# This script packages the application with all reports for deployment

set -e

# Configuration
DATE=$(date +%Y%m%d-%H%M%S)
PACKAGE_NAME="deployment-package-${DATE}.zip"
REPORTS_DIR="reports"

echo "========================================="
echo "Creating Deployment Package"
echo "========================================="
echo "Package name: ${PACKAGE_NAME}"
echo "Date: $(date)"
echo ""

# Create reports directory if it doesn't exist
mkdir -p ${REPORTS_DIR}

# Run tests with coverage
echo "Running tests with coverage..."
pytest app/tests/ --cov=app --cov-report=xml --cov-report=html --cov-report=term-missing --cov-fail-under=75
coverage report > ${REPORTS_DIR}/coverage-report.txt

# Run pylint
echo "Running pylint..."
pylint app/ --rcfile=.pylintrc --output-format=text | tee ${REPORTS_DIR}/pylint-report.txt || true

# Run bandit security scan
echo "Running bandit security scan..."
bandit -r app/ -f json -o ${REPORTS_DIR}/bandit-report.json || true
bandit -r app/ -f txt -o ${REPORTS_DIR}/bandit-report.txt || true

# Copy coverage HTML report
if [ -d "htmlcov" ]; then
    cp -r htmlcov ${REPORTS_DIR}/
fi

# Create the deployment package
echo ""
echo "Creating deployment package..."
zip -r ${PACKAGE_NAME} \
    app/ \
    requirements.txt \
    Dockerfile \
    docker-compose.yml \
    .env.example \
    pytest.ini \
    .pylintrc \
    README.md \
    ${REPORTS_DIR}/ \
    -x "*.pyc" "*.pyo" "*__pycache__*" "*.git*"

# Display package info
echo ""
echo "========================================="
echo "Deployment Package Created Successfully!"
echo "========================================="
ls -lh ${PACKAGE_NAME}
echo ""
echo "Package location: $(pwd)/${PACKAGE_NAME}"
echo ""
echo "Package contents:"
unzip -l ${PACKAGE_NAME} | head -20
echo ""
echo "Done!"
