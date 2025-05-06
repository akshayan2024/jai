# JAI API - Jyotish Astrological Interpretation API

A comprehensive REST API for Vedic (Jyotish) astrological calculations based on Swiss Ephemeris.

## Features

- **Ascendant calculation** - Calculate the ascendant (lagna) sign and degree
- **Natal Chart (D1)** - Calculate the full D1 chart with planet positions
- **Divisional Charts** - Calculate D1-D60 charts with Whole Sign house system
- **Vimshottari Mahadasha** - Calculate dasha periods with antardasha sub-periods
- **Lahiri Ayanamsa** - Uses Lahiri ayanamsa by default (configurable)
- **Retrograde Detection** - Automatically flags retrograde planets
- **1-Based Indexing** - Uses 1-based indexing for all calculations

## API Endpoints

- `/v1/api/ascendant` - Calculate ascendant sign and degree
- `/v1/api/natal-chart` - Calculate D1 natal chart
- `/v1/api/divisional-chart` - Calculate divisional charts (D1-D60)
- `/v1/api/mahadasha` - Calculate Vimshottari Mahadasha periods
- `/health` - Health check endpoint
- `/v1/docs` - OpenAPI documentation

## Technical Stack

- **Framework**: FastAPI
- **Calculation Engine**: Swiss Ephemeris
- **Deployment**: Docker, Render.com
- **Documentation**: OpenAPI 3.0

## Getting Started

### Prerequisites

- Python 3.9+
- Docker (optional)

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/jai-api.git
   cd jai-api
   ```

2. Install dependencies:
   ```
   pip install -r requirements/dev.txt
   ```

3. Run the development server:
   ```
   uvicorn main:app --reload
   ```

4. Open [http://localhost:8000/v1/docs](http://localhost:8000/v1/docs) in your browser to see the API documentation.

### Using Docker

1. Build and start the container:
   ```
   cd docker
   docker-compose up
   ```

2. Access the API at [http://localhost:8000](http://localhost:8000)

## Example API Usage

### Calculate Ascendant

```bash
curl -X POST "http://localhost:8000/v1/api/ascendant" \
  -H "Content-Type: application/json" \
  -d '{
    "birth_date": "1990-01-01",
    "birth_time": "12:00:00",
    "latitude": 28.6139,
    "longitude": 77.2090,
    "timezone_offset": 5.5,
    "ayanamsa": "lahiri"
  }'
```

## Documentation

The API documentation is available at the `/v1/docs` endpoint. It provides detailed information about all API endpoints, request parameters, and response formats.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Swiss Ephemeris for planetary calculations
- Parashara's Hora Shastra for divisional chart mappings
- FastAPI for the API framework 