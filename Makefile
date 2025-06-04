.PHONY: install test lint format check-style check-types check-security clean help

# Variables
PYTHON = python
PIP = pip
PYTEST = pytest
FLAKE8 = flake8
BLACK = black
MYPY = mypy
BANDIT = bandit
SAFETY = safety

# Default target
help:
	@echo "Available targets:"
	@echo "  install     Install development dependencies"
	@echo "  test       Run tests"
	@echo "  lint       Run linters"
	@echo "  format     Format code"
	@echo "  check      Run all checks (lint, format, types, security)"
	@echo "  check-style  Check code style"
	@echo "  check-types  Check type hints"
	@echo "  check-security  Check for security issues"
	@echo "  clean      Clean up temporary files"

# Install dependencies
install:
	$(PIP) install -e .
	$(PIP) install -r requirements-dev.txt
	pre-commit install

# Run tests
test:
	$(PYTEST) tests/ -v --cov=api --cov-report=term-missing

# Run linters
lint:
	$(FLAKE8 api/

# Format code
format:
	$(BLACK) api/ tests/

# Run all checks
check: check-style check-types check-security

# Check code style
check-style:
	$(BLACK) --check api/ tests/
	$(FLAKE8) api/ tests/

# Check type hints
check-types:
	$(MYPY) api/

# Check for security issues
check-security:
	$(BANDIT) -r api/
	$(SAFETY) check

# Clean up
clean:
	find . -type d -name "__pycache__" -exec rm -r {} +
	find . -type d -name ".mypy_cache" -exec rm -r {} +
	find . -type d -name ".pytest_cache" -exec rm -r {} +
	rm -rf .coverage htmlcov/ build/ dist/ *.egg-info/

# Run pre-commit on all files
pre-commit-all:
	pre-commit run --all-files

# Update dependencies
update-deps:
	$(PIP) install --upgrade pip
	$(PIP) install --upgrade -r requirements.txt -r requirements-dev.txt

# Run the application
dev:
	uvicorn api.main:app --reload

# Run production server
prod:
	gunicorn -c gunicorn.conf.py api.main:app
