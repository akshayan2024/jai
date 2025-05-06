# JAI API Developer Setup Guide

This guide provides step-by-step instructions for setting up your development environment for the JAI API.

## System Requirements

- Python 3.9 or higher
- pip (Python package installer)
- Git
- Docker (optional, for containerized development)

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/your-organization/jai-api.git
cd jai-api
```

### 2. Set Up a Virtual Environment

#### On Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

#### On macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

#### Development Dependencies:
```bash
pip install -r requirements/dev.txt
```

#### Production Dependencies:
```bash
pip install -r requirements/prod.txt
```

### 4. Environment Configuration

Create a `.env` file in the project root:

```
# App settings
APP_ENV=development
LOG_LEVEL=DEBUG

# API settings
API_TITLE=JAI API
API_VERSION=1.0.0
API_DESCRIPTION=Jyotish Astrological Interpretation API
API_PREFIX=/v1

# Swiss Ephemeris settings
SWEPH_PATH=./ephemeris
```

### 5. Install Swiss Ephemeris Files

Download ephemeris files:

```bash
# Create ephemeris directory
mkdir -p ephemeris

# Download ephemeris files (example)
cd ephemeris
wget https://www.astro.com/ftp/swisseph/ephe/sepl_18.se1
wget https://www.astro.com/ftp/swisseph/ephe/semo_18.se1
wget https://www.astro.com/ftp/swisseph/ephe/sepl_24.se1
wget https://www.astro.com/ftp/swisseph/ephe/semo_24.se1
cd ..
```

## Running the Application

### Start the API (Development Mode)

```bash
uvicorn jai_api.main:app --reload
```

The API will be available at http://localhost:8000.

### API Documentation

- Swagger UI: http://localhost:8000/v1/docs
- ReDoc: http://localhost:8000/v1/redoc

## Running Tests

### Run All Tests

```bash
pytest
```

### Run Tests with Coverage

```bash
pytest --cov=jai_api
```

### Run Specific Test File

```bash
pytest jai_api/tests/test_natal_chart_service.py
```

### Run Specific Test

```bash
pytest jai_api/tests/test_natal_chart_service.py::test_calculate_natal_chart
```

## Docker Development

### Build and Run with Docker Compose

```bash
docker-compose -f docker/docker-compose.dev.yml up --build
```

### Run Tests in Docker

```bash
docker-compose -f docker/docker-compose.dev.yml run --rm api pytest
```

## Common Development Tasks

### Adding a New Dependency

1. Add the dependency to the appropriate requirements file
2. Update your virtual environment:
   ```bash
   pip install -r requirements/dev.txt
   ```

### Creating a New Service

1. Create a new file in the `services` directory
2. Implement the service functions
3. Create corresponding test file in `tests` directory

### Adding a New API Endpoint

1. Create or update a file in the `routes` directory
2. Register the router in `main.py`
3. Add appropriate tests

### Working with Constants

1. Add new constants to the appropriate file in the `constants` directory
2. Update the `__init__.py` file to include the new constants in the cache

## Troubleshooting

### Import Errors

If you encounter import errors while running tests:

1. Make sure you're running tests from the project root
2. Use absolute imports in test files: `from jai_api.services import ...`
3. Check that `conftest.py` is properly configured

### Swiss Ephemeris Issues

If you encounter Swiss Ephemeris errors:

1. Verify the ephemeris files are in the correct location
2. Check that the `SWEPH_PATH` environment variable is correctly set
3. Try using absolute paths for the ephemeris directory

### Docker Container Issues

If you encounter issues with Docker:

1. Check the logs: `docker-compose logs`
2. Rebuild the containers: `docker-compose build --no-cache`
3. Check the Docker configuration files in the `docker` directory

## Code Style Guidelines

- Follow PEP 8 style guidelines
- Use type hints for function parameters and return values
- Write docstrings for all modules, classes, and functions
- Keep functions small and focused on a single responsibility

## Getting Help

If you need additional help, please:

1. Check the project documentation in the `docs` directory
2. Look for similar issues in the issue tracker
3. Ask questions in the project's communication channels
4. Contact the project maintainers 