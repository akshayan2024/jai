import pytest
from fastapi.testclient import TestClient
from datetime import datetime
from api.main import create_app
from api.models.astrological import Sign, Planet

client = TestClient(create_app())

def test_get_horoscope():
    """Test the complete horoscope endpoint"""
    birth_data = {
        "date": "1990-01-01T12:00:00",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata"
    }
    
    response = client.post("/v1/api/horoscope/", json=birth_data)
    assert response.status_code == 200
    
    data = response.json()
    
    # Check birth data
    assert data["birth_data"]["date"] == birth_data["date"]
    assert data["birth_data"]["latitude"] == birth_data["latitude"]
    assert data["birth_data"]["longitude"] == birth_data["longitude"]
    assert data["birth_data"]["timezone"] == birth_data["timezone"]
    
    # Check ascendant
    assert "sign" in data["ascendant"]
    assert "degree" in data["ascendant"]
    assert 1 <= data["ascendant"]["sign"] <= 12
    assert 0 <= data["ascendant"]["degree"] < 30
    
    # Check planets
    assert len(data["planets"]) > 0
    for planet in data["planets"]:
        assert "planet" in planet
        assert "sign" in planet
        assert "degree" in planet
        assert "is_retrograde" in planet
        assert 1 <= planet["sign"] <= 12
        assert 0 <= planet["degree"] < 30
    
    # Check houses
    assert len(data["houses"]) == 12
    for house in data["houses"]:
        assert "house_number" in house
        assert "sign" in house
        assert "degree" in house
        assert 1 <= house["house_number"] <= 12
        assert 1 <= house["sign"] <= 12
        assert 0 <= house["degree"] < 30

def test_get_horoscope_invalid_date():
    """Test horoscope endpoint with invalid date"""
    birth_data = {
        "date": "invalid-date",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata"
    }
    
    response = client.post("/v1/api/horoscope/", json=birth_data)
    assert response.status_code == 422

def test_get_horoscope_invalid_coordinates():
    """Test horoscope endpoint with invalid coordinates"""
    birth_data = {
        "date": "1990-01-01T12:00:00",
        "latitude": 200,  # Invalid latitude
        "longitude": 77.2090,
        "timezone": "Asia/Kolkata"
    }
    
    response = client.post("/v1/api/horoscope/", json=birth_data)
    assert response.status_code == 422

def test_get_horoscope_missing_data():
    """Test horoscope endpoint with missing data"""
    birth_data = {
        "date": "1990-01-01T12:00:00",
        "latitude": 28.6139
        # Missing longitude and timezone
    }
    
    response = client.post("/v1/api/horoscope/", json=birth_data)
    assert response.status_code == 422 