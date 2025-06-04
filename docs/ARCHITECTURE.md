# JAI API Architecture Reference

This document provides a comprehensive architectural overview of the JAI API system, detailing the components, data flow, and design patterns used in the implementation.

## System Overview

The JAI API is structured as a modular, service-oriented application built on FastAPI. The system is designed to perform complex Vedic astrological calculations while maintaining clean separation of concerns between different functional areas.

```
┌───────────────┐     ┌───────────────┐     ┌───────────────┐
│   Client      │────▶│   API Layer   │────▶│  Services     │
│  Applications │◀────│   (Routes)    │◀────│               │
└───────────────┘     └───────────────┘     └───────┬───────┘
                                                   │
                                                   ▼
                                           ┌───────────────┐
                                           │  Constants &  │
                                           │   Utilities   │
                                           └───────┬───────┘
                                                   │
                                                   ▼
                                           ┌───────────────┐
                                           │ Swiss Ephe.   │
                                           │ Integration   │
                                           └───────────────┘
```

## Core Components

### 1. API Layer (Routes)

**Purpose**: Handles HTTP requests, input validation, and response formatting.

**Key Components**:
- `routes/health.py`: Health check endpoint
- `routes/ascendant.py`: Ascendant calculation endpoints
- `routes/natal_chart.py`: Natal chart (D1) calculation endpoints
- `routes/divisional_charts.py`: Divisional charts (D2-D60) endpoints
- `routes/mahadasha.py`: Mahadasha calculation endpoints

**Design Patterns**:
- Request/Response models using Pydantic
- Dependency Injection for shared services
- Error handling middleware

### 2. Service Layer

**Purpose**: Implements astrological calculation logic and business rules.

**Key Components**:
- `services/ephemeris_service.py`: Swiss Ephemeris integration
- `services/ascendant_service.py`: Ascendant calculations
- `services/natal_chart_service.py`: Birth chart calculations
- `services/divisional_chart_service.py`: Divisional chart calculations
- `services/mahadasha_service.py`: Dasha period calculations

**Design Patterns**:
- Separation of concerns
- Service composition
- Pure functions for calculations

### 3. Constants and Configuration

**Purpose**: Stores astrological constants and application configuration.

**Key Components**:
- `constants/zodiac_signs.py`: Zodiac sign definitions
- `constants/planets.py`: Planet definitions
- `api/constants/nakshatras.py`: Consolidated nakshatra definitions and utilities
- `constants/ayanamsa.py`: Ayanamsa definitions
- `constants/dasha_years.py`: Mahadasha period definitions
- `constants/divisional_mappings/`: Divisional chart mapping constants
- `config.py`: Application configuration

**Nakshatra Constants Structure**:

```python
# Centralized nakshatra data structure
NAKSHATRAS: Dict[int, NakshatraData] = {
    1: {
        'name': 'Ashwini',
        'lord': 'ketu',
        'start_deg': 0.0,
        'end_deg': 13.3333,
        'pada_length': 3.3333
    },
    # ... other nakshatras
}
```

**Design Patterns**:
- Immutable constants
- Single source of truth
- Constants caching for performance
- Derived values computed from source data
- Type hints for better IDE support and code clarity

**Key Functions**:
- `get_nakshatra_index(longitude)`: Calculate nakshatra from zodiacal longitude
- `get_nakshatra_name(index)`: Get nakshatra name by index (1-27)
- `get_nakshatra_lord(index)`: Get ruling planet of a nakshatra
- `get_nakshatra_pada(longitude)`: Calculate pada (1-4) within a nakshatra
- `get_degrees_in_nakshatra(longitude)`: Get degrees within current nakshatra

**Usage Example**:
```python
# Get nakshatra information for a given longitude
longitude = 23.5  # degrees
nakshatra_idx = get_nakshatra_index(longitude)
name = get_nakshatra_name(nakshatra_idx)
lord = get_nakshatra_lord(nakshatra_idx)
pada = get_nakshatra_pada(longitude)
degrees = get_degrees_in_nakshatra(longitude)
```

### 4. Utilities

**Purpose**: Provides shared helper functions and cross-cutting concerns.

**Key Components**:
- `utils/logger.py`: Logging configuration
- `utils/custom_exceptions.py`: Custom exception definitions
- `utils/error_handlers.py`: Global error handling
- `utils/date_utils.py`: Date and time conversions
- `utils/validation.py`: Input validation helpers

**Design Patterns**:
- Cross-cutting concerns
- Centralized error handling
- Standardized logging

### 5. Swiss Ephemeris Integration

**Purpose**: Interfaces with the Swiss Ephemeris library for astronomical calculations.

**Key Components**:
- `services/ephemeris_service.py`: Wrapper around Swiss Ephemeris
- `services/ephemeris_stub.py`: Test stub for development and testing

**Design Patterns**:
- Adapter pattern
- Dependency inversion
- Interface segregation

## Data Flow

### Basic Chart Calculation Flow

1. **Client Request**: Client sends birth data to API endpoint
2. **Input Validation**: API validates input parameters
3. **Julian Day Conversion**: Date and time converted to Julian day
4. **Ephemeris Calculation**: Swiss Ephemeris calculates planetary positions
5. **Ayanamsa Adjustment**: Positions adjusted according to ayanamsa
6. **Chart Construction**: Natal chart constructed from planetary positions
7. **Response Formatting**: API formats and returns chart data

```
┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐     ┌─────────┐
│  Input  │────▶│ Convert │────▶│Calculate│────▶│ Adjust  │────▶│ Format  │
│ Params  │     │   to    │     │ Planet  │     │   for   │     │ Response│
│         │     │Julian Day│     │Positions│     │Ayanamsa │     │         │
└─────────┘     └─────────┘     └─────────┘     └─────────┘     └─────────┘
```

### Divisional Chart Calculation Flow

1. **Natal Chart**: Calculate complete natal chart (D1)
2. **Division Calculation**: Calculate division within each sign
3. **Mapping Application**: Apply divisional mapping rules
4. **House Assignment**: Assign houses in the divisional chart
5. **Response Construction**: Combine all divisional chart data

### Mahadasha Calculation Flow

1. **Moon Position**: Calculate exact Moon position at birth
2. **Nakshatra Determination**: Determine Moon's nakshatra
3. **Period Calculation**: Calculate mahadasha sequence and timing
4. **Balance Calculation**: Calculate remaining balance of first period
5. **Sub-period Calculation**: Calculate antardashas within each mahadasha

## Data Models

### Input Models

- **BirthDataRequest**: Birth date, time, location for chart calculation
- **AyanamsaOption**: Ayanamsa selection for calculations
- **DivisionalChartRequest**: Request for specific divisional charts

### Response Models

- **PlanetPosition**: Position data for a single planet
- **NatalChart**: Complete birth chart with all planets
- **DivisionalChart**: Divisional chart data for specific divisional chart
- **MahadashaPeriod**: Single mahadasha period data
- **MahadashaResponse**: Complete mahadasha sequence

## Cross-Cutting Concerns

### Error Handling

- **Global Exception Handler**: Catches and formats all exceptions
- **Custom Exceptions**: Domain-specific exceptions (CalculationError, ValidationError)
- **Structured Error Responses**: Consistent JSON error format

### Logging

- **Structured Logging**: JSON format logs with context
- **Log Levels**: DEBUG, INFO, WARNING, ERROR
- **Log Rotation**: Size-based rotation for log files

### Performance Optimization

- **Constants Caching**: One-time loading of astrological constants
- **Calculation Optimization**: Efficient algorithms for chart calculations
- **Service Composition**: Minimize duplication of calculations

## Deployment Architecture

### Docker-based Deployment

```
┌─────────────────────────────────────────┐
│              Docker Host                │
│                                         │
│  ┌─────────────┐     ┌─────────────┐    │
│  │   JAI API   │     │   Logging   │    │
│  │  Container  │─────│  Container  │    │
│  └─────────────┘     └─────────────┘    │
│                                         │
└─────────────────────────────────────────┘
```

### Cloud Deployment (Render.com)

- **Web Service**: JAI API FastAPI application
- **Environment Variables**: Configuration via environment
- **Auto-deployment**: Connected to GitHub repository
- **Logging**: Integrated with Render logging dashboard

## Testing Architecture

- **Unit Tests**: Test individual service functions
- **Integration Tests**: Test API endpoints end-to-end
- **Test Fixtures**: Common test data in conftest.py
- **Mocking**: Mock Swiss Ephemeris for deterministic tests

## Security Considerations

- **Input Validation**: Thorough validation of all inputs
- **Error Hiding**: Internal errors not exposed to clients
- **Rate Limiting**: Future addition for public API endpoints
- **Authentication**: Future addition for protected endpoints

## Future Architecture Enhancements

- **Caching Layer**: Redis cache for frequently requested charts
- **Database Integration**: Store calculation results for analysis
- **Worker Processes**: Background workers for intensive calculations
- **GraphQL API**: Alternative API interface for complex queries

## Appendix: Component Dependencies

```
┌─────────────────┐
│   API Routes    │
└───────┬─────────┘
        │
        ▼
┌─────────────────┐     ┌─────────────────┐
│    Services     │────▶│    Constants    │
└───────┬─────────┘     └─────────────────┘
        │
        ▼
┌─────────────────┐     ┌─────────────────┐
│  Swiss Ephe.    │────▶│    Utilities    │
└─────────────────┘     └─────────────────┘
``` 