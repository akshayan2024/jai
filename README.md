# JAI (Jyotish Astrological Interpretation) API

A modern API for Vedic astrology calculations and interpretations.

## Overview

JAI API provides a comprehensive set of endpoints for Vedic astrology calculations, including:

- Basic birth chart (D-1) calculations
- Divisional charts (D-9, D-10, etc.)
- Planetary positions and aspects
- Dasha periods (Mahadasha, Antardasha, Pratyantardasha)
- Yoga formations
- Transit calculations
- House positions and aspects

## Project Structure

```
E:/jai/
├── api/                    # API code directory
│   ├── main.py             # Main FastAPI application
│   ├── models/             # Data models
│   │   ├── request.py      # Request models
│   │   └── response.py     # Response models
│   ├── routes/             # API routes
│   │   ├── ascendant.py    # Ascendant endpoints
│   │   ├── planets.py      # Planets endpoints 
│   │   └── ...             # Other endpoint modules
│   └── services/           # Business logic
│       ├── calculation.py  # Core calculation logic
│       └── validation.py   # Input validation
├── tests/                  # Test directory
│   ├── test_api.py         # API tests
│   └── test_server.py      # Mock server for testing
├── utils/                  # Utility functions
│   └── constants.py        # Astrological constants
├── requirements.txt        # Dependencies
├── run.py                  # Script to run the application
└── README.md               # This file
```

## Setup and Installation

1. Clone the repository:
```
git clone https://github.com/yourusername/jai.git
cd jai
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Run the application:
```
python run.py
```

The API will be available at `http://localhost:8000`.

## API Documentation

Once the application is running, you can access the auto-generated API documentation at:
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## Testing

Run the tests with:
```
python -m pytest tests/
```

## Usage Examples

### Calculate Birth Chart
```python
import requests

# Chennai birth data
birth_data = {
    "birth_date": "1988-12-01",
    "birth_time": "21:47:00",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone_offset": 5.5,
    "ayanamsa": "lahiri"
}

response = requests.post("http://localhost:8000/v1/api/horoscope", json=birth_data)
print(response.json())
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 