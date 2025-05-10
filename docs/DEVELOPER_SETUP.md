# Developer Setup Guide

## Prerequisites

- Python 3.8 or higher
- pip (Python package installer)
- Git

## Installation Steps

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jai-api.git
cd jai-api
```

2. Create and activate a virtual environment:
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# Linux/Mac
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Download Swiss Ephemeris files:
```bash
# Windows
.\download_ephemeris.ps1

# Linux/Mac
./download_ephemeris.sh
```

The script will download and extract the required Swiss Ephemeris files to the `ephemeris` directory.

## Running the API

1. Start the development server:
```bash
uvicorn api.main:app --reload
```

2. Access the API documentation:
- OpenAPI (Swagger) UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Running Tests

```bash
pytest
```

## Development Notes

### Swiss Ephemeris

The project uses `pyswisseph` (version 2.10.3.2) for astrological calculations. The required ephemeris files are:

- `sepl.se1`: Main ephemeris file
- `seplm.se1`: Main ephemeris file (modern)
- `seas.se1`: Asteroids ephemeris
- `semo.se1`: Moon ephemeris
- `fixstars.cat`: Fixed stars catalog
- `seasnam.txt`: Asteroid names
- `sefstars.txt`: Fixed star names

These files are automatically downloaded and placed in the `ephemeris` directory by the setup scripts.

### Mock Implementation

For testing purposes, a mock implementation of the Swiss Ephemeris is provided in `api/services/mock_swisseph.py`. This mock can be enabled/disabled using:

```python
from api.services.mock_swisseph import enable_mock, disable_mock

# Enable mock for testing
enable_mock()

# Disable mock to use real Swiss Ephemeris
disable_mock()
```

### Environment Variables

Create a `.env` file in the project root with the following variables:

```env
EPHEMERIS_PATH=./ephemeris
DEBUG=True
```

## Contributing

1. Create a new branch for your feature/fix
2. Make your changes
3. Add tests for your changes
4. Run the test suite
5. Submit a pull request

## Troubleshooting

### Common Issues

1. **Missing Ephemeris Files**
   - Ensure the `ephemeris` directory exists
   - Run the download script again
   - Check file permissions

2. **Import Errors**
   - Verify virtual environment is activated
   - Check Python version (3.8+ required)
   - Reinstall dependencies: `pip install -r requirements.txt`

3. **Calculation Errors**
   - Verify ephemeris files are present
   - Check file permissions
   - Ensure correct ayanamsa setting

### Getting Help

- Check the [API Documentation](http://localhost:8000/docs)
- Review the [OpenAPI Specification](openapi-schema.yaml)
- Open an issue on GitHub 