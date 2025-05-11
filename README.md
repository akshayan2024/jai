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

All calculations are performed using the Swiss Ephemeris library for astronomical accuracy.

## Key Features

- **Accurate Astronomical Calculations**: Powered by Swiss Ephemeris for precise planetary positions.
- **Multiple Ayanamsa Options**: Support for Lahiri, Raman, and Krishnamurti ayanamsa methods.
- **Geocoding Integration**: Provide a place name instead of coordinates to automatically determine birth location details.
- **Comprehensive Dasha System**: Vimshottari dasha calculations with mahadasha, antardasha, and pratyantardasha periods.
- **Caching System**: Efficient caching for geocoding and timezone data to improve performance.
- **Robust Error Handling**: Detailed error messages with appropriate HTTP status codes.

## Project Structure

```
jai/
├── api/                    # API code directory
│   ├── main.py             # Main FastAPI application
│   ├── models/             # Data models
│   │   ├── request.py      # Request models
│   │   └── response.py     # Response models
│   ├── routes/             # API routes
│   │   ├── __init__.py     # Router initialization
│   │   ├── ascendant.py    # Ascendant endpoints
│   │   └── planets.py      # Planets endpoints
│   ├── services/           # Business logic
│   │   ├── __init__.py     # Service initialization
│   │   └── calculation.py  # Core calculation logic
│   └── utils/              # Utility functions
│       ├── error_handling.py # Error handling utilities
│       └── input_parser.py   # Input parsing utilities
├── constants/              # Astrological constants
│   ├── __init__.py         # Constants initialization
│   ├── zodiac_signs.py     # Zodiac sign constants
│   ├── nakshatras.py       # Nakshatra constants
│   └── divisional_mappings/ # Divisional chart mappings
├── docs/                   # Documentation
│   ├── USER_STORIES.md     # User stories
│   └── ARCHITECTURE.md     # Architecture documentation
├── ephemeris/              # Swiss Ephemeris data files
├── tests/                  # Test directory
│   ├── __init__.py         # Test initialization
│   ├── test_api.py         # API tests
│   └── test_componentized.py # Component tests
├── cache/                  # Cache directory for geocoding/timezone
├── run.py                  # Entry point to run the application
├── requirements.txt        # Dependencies
├── Dockerfile              # Docker configuration
├── docker-compose.yml      # Docker Compose configuration
└── README.md               # This file
```

## Prerequisites

- Python 3.8+
- Swiss Ephemeris library
- FastAPI and dependencies

## Setup and Installation

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/yourusername/jai.git
cd jai
```

2. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables (optional):
```bash
# For TimeZoneDB API (optional, falls back to approximate calculation)
export TIMEZONEDB_API_KEY=your_api_key_here

# For ephemeris path (optional, defaults to ./ephemeris)
export EPHEMERIS_PATH=/path/to/ephemeris
```

5. Run the application:
```bash
python run.py
```

The API will be available at `http://localhost:8000`.

### Docker Deployment

1. Build the Docker image:
```bash
docker build -t jai-api .
```

2. Run the container:
```bash
docker run -p 8000:8000 -e TIMEZONEDB_API_KEY=your_api_key_here jai-api
```

Alternatively, use Docker Compose:
```bash
docker-compose up
```

## API Documentation

Once the application is running, you can access the auto-generated API documentation at:
- Swagger UI: `http://localhost:8000/v1/docs`
- ReDoc: `http://localhost:8000/v1/redoc`

## Usage Examples

### Calculate Birth Chart
```python
import requests

# Example with place name (preferred method)
birth_data = {
    "birth_date": "1988-12-01",
    "birth_time": "21:47:00",
    "place": "Chennai, India",
    "ayanamsa": "lahiri"
}

response = requests.post("http://localhost:8000/v1/api/horoscope", json=birth_data)
print(response.json())
```

### Alternative Method (with coordinates)
```python
import requests

# Alternative with manual coordinates
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

## Testing

Run tests with pytest:
```bash
python -m pytest
```

For more information on testing, see [tests/README.md](tests/README.md).

## Error Handling

The API follows standard HTTP status codes:
- 200: Successful operation
- 400: Bad request (invalid input)
- 404: Resource not found
- 429: Too many requests (rate limiting)
- 500: Internal server error

Error responses include detailed messages to help diagnose issues.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Production Deployment

To deploy this API in production, ensure the following:

1. **Swiss Ephemeris**
   - Install the Swiss Ephemeris C library and data files.
   - Install the Python package: `pip install pyswisseph`
   - Download ephemeris data files from [Swiss Ephemeris downloads](https://www.astro.com/ftp/swisseph/) and set the path using the `EPHEMERIS_PATH` environment variable.

2. **Environment Variables**
   - `EPHEMERIS_PATH`: Path to Swiss Ephemeris data files (e.g., `./ephemeris`)
   - `OPENCAGE_API_KEY`: Your OpenCage geocoding API key (required for place-based lookups)
   - `ALLOWED_ORIGINS`: Comma-separated list of allowed CORS origins (e.g., `https://yourdomain.com,https://app.yourdomain.com`)

3. **Security & Rate Limiting**
   - CORS is restricted to trusted origins via `ALLOWED_ORIGINS`.
   - Rate limiting is enabled (60 requests/minute per IP).
   - All sensitive keys must be set via environment variables, never hardcoded.

4. **Testing**
   - Ensure all endpoints work with both coordinate and place-based input.
   - Check logs for any warnings or errors.

## ChatGPT Actions Integration

This API is specially designed for seamless integration with ChatGPT Actions, allowing your LLM applications to perform Vedic astrology calculations based on user inputs.

### How It Works

1. When a user asks a question related to Vedic astrology (e.g., "What's my rising sign? I was born on June 15, 1990 at 3:45 PM in Chicago"), ChatGPT can:
   - Extract the birth date, time, and place from the natural language query
   - Format these details appropriately for the API
   - Call the relevant endpoint to calculate the requested astrological information
   - Present the results in a user-friendly manner

### API Features for ChatGPT

- **Flexible Input Formats**: Accepts various date and time formats (e.g., "June 15, 1990", "3:45 PM")
- **Place-based Geocoding**: Use natural location names (cities, countries) instead of requiring latitude/longitude
- **Comprehensive Endpoints**: Calculate ascendants, planetary positions, divisional charts, and more
- **Standardized Responses**: Clean, well-structured JSON responses for easy parsing by LLMs

### Example Integration

```js
// Example of how to use the API with ChatGPT Actions
const userQuery = "What's my rising sign? I was born on June 15, 1990 at 3:45 PM in Chicago";

// ChatGPT extracts information from the query
const birthData = {
  birth_date: "1990-06-15",  // Parsed from "June 15, 1990"
  birth_time: "15:45:00",    // Parsed from "3:45 PM" 
  place: "Chicago, USA"      // Extracted from query
};

// ChatGPT calls the API
const response = await fetch("https://jai-api.onrender.com/v1/api/horoscope/ascendant", {
  method: "POST",
  headers: { "Content-Type": "application/json" },
  body: JSON.stringify(birthData)
});

const result = await response.json();
// ChatGPT can now interpret and explain the results to the user
```

### OpenAPI Specification

The API includes a detailed OpenAPI specification (`gpt.yaml`) that documents all endpoints, request formats, and response structures. This specification can be used to register the API as a ChatGPT Action. 