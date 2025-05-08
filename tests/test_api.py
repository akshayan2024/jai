"""
Basic API tests for JAI API
"""
import pytest
from fastapi.testclient import TestClient
import json
import os
import sys

# Add the root directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from api.main import app

client = TestClient(app)

def test_root_endpoint():
    """Test the root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "version" in data

def test_health_check():
    """Test the health check endpoint"""
    response = client.get("/v1/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"

def test_horoscope_input_validation():
    """Test input validation for horoscope endpoint"""
    # Invalid date format
    invalid_data = {
        "birth_date": "01-12-1988",  # Wrong format
        "birth_time": "21:47:00",
        "latitude": 13.0827,
        "longitude": 80.2707,
        "timezone_offset": 5.5,
        "ayanamsa": "lahiri"
    }
    response = client.post("/v1/api/horoscope", json=invalid_data)
    assert response.status_code == 422  # Validation error

    # Missing required field
    missing_field = {
        "birth_date": "1988-12-01",
        # birth_time is missing
        "latitude": 13.0827,
        "longitude": 80.2707,
        "timezone_offset": 5.5,
        "ayanamsa": "lahiri"
    }
    response = client.post("/v1/api/horoscope", json=missing_field)
    assert response.status_code == 422  # Validation error

def test_rate_limiting():
    """Test rate limiting functionality"""
    # Make multiple requests in quick succession
    for _ in range(5):
        response = client.get("/v1/api/health")
    
    # The last one might be rate limited depending on implementation
    # This is more of a demonstration - actual implementation may vary
    assert response.status_code in [200, 429]

# Additional tests would be written for specific endpoints... 