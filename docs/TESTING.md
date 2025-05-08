# JAI API Testing Strategy

This document outlines the testing strategy for the JAI API, including testing levels, test types, and implementation guidelines.

## Testing Levels

### 1. Unit Testing

Unit tests verify individual components in isolation.

**Focus Areas:**
- Service functions
- Utility functions
- Model validations
- Constants validation

**Implementation:**
- All unit tests are in `tests/` directory with `test_` prefix
- Each module has a corresponding test file
- Tests use pytest fixtures for common test data
- Constants are loaded once per test session

### 2. Integration Testing

Integration tests verify that components work together correctly.

**Focus Areas:**
- API endpoints
- Service interactions
- Data flow through the system

**Implementation:**
- Tests use FastAPI TestClient
- Test data includes edge cases and typical usage patterns
- Database interactions are mocked or use test databases

### 3. Validation Testing

Validation tests verify astrological calculations against known reference values.

**Focus Areas:**
- Planet positions
- Ascendant calculations
- Divisional chart mappings
- Mahadasha calculations

**Implementation:**
- Tests compare results against known accurate values
- Reference data sourced from established astrological software
- Acceptable margin of error defined for floating-point comparisons

## Test Types

### Functional Tests

Verify that the system performs its required functions correctly.

**Examples:**
- Birth chart generation
- Divisional chart calculations
- Mahadasha calculations
- Ayanamsa adjustments

### Edge Case Tests

Verify system behavior with boundary values and extreme inputs.

**Examples:**
- Birth dates at year boundaries
- Positions at 0° and 360°
- Planets at sign boundaries
- Retrograde transitions

### Error Handling Tests

Verify that the system handles errors gracefully.

**Examples:**
- Invalid input validation
- Missing required parameters
- Out-of-range values
- Unsupported chart types

### Performance Tests

Verify that the system meets performance requirements.

**Examples:**
- Response time for chart calculations
- Multiple concurrent requests
- Resource utilization

## Test Implementation Guidelines

### Test Structure

Each test module should follow this structure:
1. Imports and fixtures
2. Setup functions (if needed)
3. Test cases grouped by functionality
4. Helpers and utilities at the end

### Test Fixtures

Common test fixtures are defined in `conftest.py`:
- Birth data samples
- Natal chart positions
- Constants loading

### Assertions

Tests should use specific assertions with clear error messages:
- `assert result == expected, f"Expected {expected}, got {result}"`
- Use `pytest.approx()` for floating-point comparisons

### Mocking

External dependencies should be mocked:
- Swiss Ephemeris calls
- External APIs
- File I/O operations
- Database operations

## Test Execution

### Local Development

Run tests during development:

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_natal_chart_service.py

# Run specific test
pytest tests/test_natal_chart_service.py::test_calculate_natal_chart
```

### Continuous Integration

Tests run automatically in the CI pipeline:
1. When creating a pull request
2. When merging to main branch
3. On scheduled intervals

### Test Coverage

Test coverage is monitored using pytest-cov:

```bash
# Generate coverage report
pytest --cov=jai_api

# Generate HTML coverage report
pytest --cov=jai_api --cov-report=html
```

**Coverage Targets:**
- 95% for core calculation modules
- 90% for services
- 85% for API routes
- 100% for constants

## Test Maintenance

### Test Data Updates

Test data should be reviewed and updated when:
- New features are added
- Calculation methods change
- Bugs are fixed

### Regression Tests

Add regression tests when fixing bugs:
1. Create a test that reproduces the bug
2. Fix the bug
3. Verify the test passes

### Performance Benchmarks

Maintain performance benchmarks:
1. Measure baseline performance
2. Track performance changes over time
3. Alert on significant performance degradation 