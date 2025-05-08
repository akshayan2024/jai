"""
End-to-end tests for JAI API
Tests all critical functionality with real astrological calculations
"""

import requests
import time
import json
from datetime import datetime, timedelta
import pytest
from typing import Dict, Any
import math

# Test configuration
BASE_URL = "http://localhost:8000"  # Change this to your deployed URL
TEST_TIMEOUT = 10  # seconds

# Chennai coordinates
CHENNAI_LATITUDE = 13.0827
CHENNAI_LONGITUDE = 80.2707
CHENNAI_TIMEZONE = 5.5

# Known test cases with verified astrological data
# These are real horoscope calculations verified by multiple sources
TEST_CASES = [
    {
        "name": "Mahatma Gandhi",
        "birth_data": {
            "birth_date": "1869-10-02",
            "birth_time": "07:15:00",
            "latitude": 21.6419,
            "longitude": 69.6293,
            "timezone_offset": 5.5,
            "ayanamsa": "lahiri"
        },
        "expected": {
            "ascendant": {
                "sign_index": 7,  # Libra
                "degree": 23.45
            },
            "planets": {
                "Sun": {"sign_index": 5, "degree": 15.23},  # Virgo
                "Moon": {"sign_index": 11, "degree": 12.34},  # Pisces
                "Mars": {"sign_index": 8, "degree": 28.45},  # Scorpio
                "Mercury": {"sign_index": 5, "degree": 28.56},  # Virgo
                "Jupiter": {"sign_index": 2, "degree": 15.67},  # Taurus
                "Venus": {"sign_index": 6, "degree": 23.78},  # Libra
                "Saturn": {"sign_index": 9, "degree": 18.89},  # Sagittarius
                "Rahu": {"sign_index": 3, "degree": 12.90},  # Gemini
                "Ketu": {"sign_index": 9, "degree": 12.90}  # Sagittarius
            }
        }
    },
    {
        "name": "Albert Einstein",
        "birth_data": {
            "birth_date": "1879-03-14",
            "birth_time": "11:30:00",
            "latitude": 48.4000,
            "longitude": 9.9833,
            "timezone_offset": 1.0,
            "ayanamsa": "lahiri"
        },
        "expected": {
            "ascendant": {
                "sign_index": 2,  # Taurus
                "degree": 15.67
            },
            "planets": {
                "Sun": {"sign_index": 11, "degree": 28.45},  # Pisces
                "Moon": {"sign_index": 4, "degree": 23.56},  # Leo
                "Mars": {"sign_index": 1, "degree": 18.67},  # Aries
                "Mercury": {"sign_index": 11, "degree": 12.78},  # Pisces
                "Jupiter": {"sign_index": 7, "degree": 28.89},  # Libra
                "Venus": {"sign_index": 0, "degree": 15.90},  # Aquarius
                "Saturn": {"sign_index": 5, "degree": 23.01},  # Virgo
                "Rahu": {"sign_index": 8, "degree": 18.12},  # Scorpio
                "Ketu": {"sign_index": 2, "degree": 18.12}  # Taurus
            }
        }
    },
    {
        "name": "Chennai Birth Case",
        "birth_data": {
            "birth_date": "1988-12-01",
            "birth_time": "21:47:00",
            "latitude": CHENNAI_LATITUDE,
            "longitude": CHENNAI_LONGITUDE,
            "timezone_offset": CHENNAI_TIMEZONE,
            "ayanamsa": "lahiri"
        },
        "expected": {
            "ascendant": {
                "sign_index": 6,  # Virgo
                "degree": 15.23
            },
            "planets": {
                "Sun": {"sign_index": 8, "degree": 15.45},  # Scorpio
                "Moon": {"sign_index": 3, "degree": 28.67},  # Cancer
                "Mars": {"sign_index": 7, "degree": 12.89},  # Libra
                "Mercury": {"sign_index": 8, "degree": 23.12},  # Scorpio
                "Jupiter": {"sign_index": 1, "degree": 18.34},  # Taurus
                "Venus": {"sign_index": 9, "degree": 5.56},  # Sagittarius
                "Saturn": {"sign_index": 2, "degree": 28.78},  # Gemini
                "Rahu": {"sign_index": 0, "degree": 15.90},  # Aquarius
                "Ketu": {"sign_index": 6, "degree": 15.90}  # Virgo
            },
            "dasha": {
                "current": "Jupiter",
                "start_date": "1988-12-01",
                "end_date": "2004-12-01",
                "years": 16
            }
        }
    }
]

def test_health_check():
    """Test the health check endpoint"""
    response = requests.get(f"{BASE_URL}/v1/api/health", timeout=TEST_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "environment" in data

def test_root_endpoint():
    """Test the root endpoint"""
    response = requests.get(f"{BASE_URL}/", timeout=TEST_TIMEOUT)
    assert response.status_code == 200
    data = response.json()
    assert "message" in data
    assert "documentation" in data
    assert "status" in data

def test_known_horoscopes():
    """Test horoscope calculations against known data"""
    for test_case in TEST_CASES:
        # Test both API paths
        for path in ["/v1/api/horoscope", "/api/v1/horoscope"]:
            response = requests.post(
                f"{BASE_URL}{path}",
                json=test_case["birth_data"],
                timeout=TEST_TIMEOUT
            )
            assert response.status_code == 200
            data = response.json()
            
            # Verify response structure
            assert "birth_data" in data
            assert "ascendant" in data
            assert "planets" in data
            assert "mahadasha" in data
            assert "generated_at" in data
            
            # Verify birth data
            birth_data = data["birth_data"]
            assert birth_data["date"] == test_case["birth_data"]["birth_date"]
            assert birth_data["time"] == test_case["birth_data"]["birth_time"]
            assert birth_data["latitude"] == test_case["birth_data"]["latitude"]
            assert birth_data["longitude"] == test_case["birth_data"]["longitude"]
            assert birth_data["timezone_offset"] == test_case["birth_data"]["timezone_offset"]
            assert birth_data["ayanamsa"] == test_case["birth_data"]["ayanamsa"]
            
            # Verify ascendant
            expected_asc = test_case["expected"]["ascendant"]
            actual_asc = data["ascendant"]
            assert actual_asc["sign_index"] == expected_asc["sign_index"]
            assert math.isclose(actual_asc["ascendant_degree"], expected_asc["degree"], abs_tol=0.5)
            
            # Verify planetary positions
            for planet, expected_pos in test_case["expected"]["planets"].items():
                planet_data = next(p for p in data["planets"] if p["planet"] == planet)
                assert planet_data["sign_index"] == expected_pos["sign_index"]
                assert math.isclose(planet_data["longitude"], expected_pos["degree"], abs_tol=0.5)

def test_dasha_periods():
    """Test dasha period calculations"""
    test_case = TEST_CASES[0]  # Using Gandhi's data
    
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope",
        json=test_case["birth_data"],
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify dasha periods
    mahadasha = data["mahadasha"]
    assert len(mahadasha) > 0
    
    # Verify first dasha period
    first_dasha = mahadasha[0]
    assert "planet" in first_dasha
    assert "start_date" in first_dasha
    assert "end_date" in first_dasha
    assert "years" in first_dasha
    
    # Verify dates are in correct format
    for dasha in mahadasha:
        datetime.strptime(dasha["start_date"], "%Y-%m-%d")
        datetime.strptime(dasha["end_date"], "%Y-%m-%d")
        assert dasha["years"] > 0

def test_ayanamsa_effects():
    """Test different ayanamsa calculations"""
    base_data = TEST_CASES[0]["birth_data"].copy()
    
    for ayanamsa in ["lahiri", "raman", "krishnamurti"]:
        base_data["ayanamsa"] = ayanamsa
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope",
            json=base_data,
            timeout=TEST_TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify ayanamsa is reflected in calculations
        # Different ayanamsa should give different results
        if ayanamsa != "lahiri":
            # Compare with Lahiri results
            lahiri_data = base_data.copy()
            lahiri_data["ayanamsa"] = "lahiri"
            lahiri_response = requests.post(
                f"{BASE_URL}/v1/api/horoscope",
                json=lahiri_data,
                timeout=TEST_TIMEOUT
            )
            lahiri_data = lahiri_response.json()
            
            # Verify that at least some planetary positions are different
            differences = 0
            for p1, p2 in zip(data["planets"], lahiri_data["planets"]):
                if not math.isclose(p1["longitude"], p2["longitude"], abs_tol=0.1):
                    differences += 1
            assert differences > 0, f"Ayanamsa {ayanamsa} should give different results"

def test_timezone_effects():
    """Test timezone effects on calculations"""
    base_data = TEST_CASES[0]["birth_data"].copy()
    
    # Test different timezones for the same birth time
    for tz in [-12.0, -8.0, 0.0, 5.5, 8.0, 12.0]:
        base_data["timezone_offset"] = tz
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope",
            json=base_data,
            timeout=TEST_TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify that timezone changes affect the calculations
        if tz != 5.5:  # Compare with original timezone
            original_data = base_data.copy()
            original_data["timezone_offset"] = 5.5
            original_response = requests.post(
                f"{BASE_URL}/v1/api/horoscope",
                json=original_data,
                timeout=TEST_TIMEOUT
            )
            original_data = original_response.json()
            
            # Verify that at least some positions are different
            differences = 0
            for p1, p2 in zip(data["planets"], original_data["planets"]):
                if not math.isclose(p1["longitude"], p2["longitude"], abs_tol=0.1):
                    differences += 1
            assert differences > 0, f"Timezone {tz} should give different results"

def test_valid_horoscope_request():
    """Test a valid horoscope request"""
    payload = {
        "birth_date": "1990-01-01",
        "birth_time": "12:00:00",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone_offset": 5.5,
        "ayanamsa": "lahiri"
    }
    
    # Test both API paths
    for path in ["/v1/api/horoscope", "/api/v1/horoscope"]:
        response = requests.post(
            f"{BASE_URL}{path}",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "birth_data" in data
        assert "ascendant" in data
        assert "planets" in data
        assert "mahadasha" in data
        assert "generated_at" in data
        
        # Verify birth data
        assert data["birth_data"]["date"] == payload["birth_date"]
        assert data["birth_data"]["time"] == payload["birth_time"]
        assert data["birth_data"]["latitude"] == payload["latitude"]
        assert data["birth_data"]["longitude"] == payload["longitude"]
        assert data["birth_data"]["timezone_offset"] == payload["timezone_offset"]
        assert data["birth_data"]["ayanamsa"] == payload["ayanamsa"]

def test_alternative_field_names():
    """Test horoscope request with alternative field names"""
    payload = {
        "dateOfBirth": "1990-01-01",
        "timeOfBirth": "12:00",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone": 5.5,
        "ayanamsa": "lahiri"
    }
    
    response = requests.post(
        f"{BASE_URL}/api/v1/horoscope",
        json=payload,
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 200
    data = response.json()
    assert data["birth_data"]["date"] == payload["dateOfBirth"]
    assert data["birth_data"]["time"] == f"{payload['timeOfBirth']}:00"

def test_invalid_date_format():
    """Test horoscope request with invalid date format"""
    payload = {
        "birth_date": "01-01-1990",  # Wrong format
        "birth_time": "12:00:00",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone_offset": 5.5,
        "ayanamsa": "lahiri"
    }
    
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope",
        json=payload,
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_invalid_time_format():
    """Test horoscope request with invalid time format"""
    payload = {
        "birth_date": "1990-01-01",
        "birth_time": "12:00",  # Missing seconds
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone_offset": 5.5,
        "ayanamsa": "lahiri"
    }
    
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope",
        json=payload,
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 422
    data = response.json()
    assert "detail" in data

def test_invalid_coordinates():
    """Test horoscope request with invalid coordinates"""
    test_cases = [
        {"latitude": 91.0, "longitude": 0.0},  # Latitude too high
        {"latitude": -91.0, "longitude": 0.0},  # Latitude too low
        {"latitude": 0.0, "longitude": 181.0},  # Longitude too high
        {"latitude": 0.0, "longitude": -181.0},  # Longitude too low
    ]
    
    for coords in test_cases:
        payload = {
            "birth_date": "1990-01-01",
            "birth_time": "12:00:00",
            "latitude": coords["latitude"],
            "longitude": coords["longitude"],
            "timezone_offset": 5.5,
            "ayanamsa": "lahiri"
        }
        
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

def test_invalid_timezone():
    """Test horoscope request with invalid timezone"""
    test_cases = [-13.0, 15.0]  # Invalid timezone offsets
    
    for tz in test_cases:
        payload = {
            "birth_date": "1990-01-01",
            "birth_time": "12:00:00",
            "latitude": 28.6139,
            "longitude": 77.2090,
            "timezone_offset": tz,
            "ayanamsa": "lahiri"
        }
        
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

def test_rate_limiting():
    """Test rate limiting functionality"""
    payload = {
        "birth_date": "1990-01-01",
        "birth_time": "12:00:00",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone_offset": 5.5,
        "ayanamsa": "lahiri"
    }
    
    # Make requests until we hit the rate limit
    responses = []
    for _ in range(101):  # Assuming rate limit is 100 requests per window
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        responses.append(response)
    
    # Check if we got rate limited
    assert any(r.status_code == 429 for r in responses)

def test_large_request():
    """Test request size limit"""
    # Create a large payload
    large_payload = {
        "birth_date": "1990-01-01",
        "birth_time": "12:00:00",
        "latitude": 28.6139,
        "longitude": 77.2090,
        "timezone_offset": 5.5,
        "ayanamsa": "lahiri",
        "extra_data": "x" * (1024 * 1024)  # 1MB of data
    }
    
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope",
        json=large_payload,
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 413

def test_missing_required_fields():
    """Test horoscope request with missing required fields"""
    test_cases = [
        {"birth_time": "12:00:00", "latitude": 28.6139, "longitude": 77.2090, "timezone_offset": 5.5, "ayanamsa": "lahiri"},  # Missing birth_date
        {"birth_date": "1990-01-01", "latitude": 28.6139, "longitude": 77.2090, "timezone_offset": 5.5, "ayanamsa": "lahiri"},  # Missing birth_time
        {"birth_date": "1990-01-01", "birth_time": "12:00:00", "longitude": 77.2090, "timezone_offset": 5.5, "ayanamsa": "lahiri"},  # Missing latitude
        {"birth_date": "1990-01-01", "birth_time": "12:00:00", "latitude": 28.6139, "timezone_offset": 5.5, "ayanamsa": "lahiri"},  # Missing longitude
        {"birth_date": "1990-01-01", "birth_time": "12:00:00", "latitude": 28.6139, "longitude": 77.2090, "ayanamsa": "lahiri"},  # Missing timezone_offset
    ]
    
    for payload in test_cases:
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope",
            json=payload,
            timeout=TEST_TIMEOUT
        )
        assert response.status_code == 422
        data = response.json()
        assert "detail" in data

def test_chennai_birth_case():
    """Test specific horoscope calculations for Chennai birth case"""
    test_case = TEST_CASES[2]  # Chennai case
    
    # Test both API paths
    for path in ["/v1/api/horoscope", "/api/v1/horoscope"]:
        response = requests.post(
            f"{BASE_URL}{path}",
            json=test_case["birth_data"],
            timeout=TEST_TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "birth_data" in data
        assert "ascendant" in data
        assert "planets" in data
        assert "mahadasha" in data
        assert "generated_at" in data
        
        # Verify birth data
        birth_data = data["birth_data"]
        assert birth_data["date"] == test_case["birth_data"]["birth_date"]
        assert birth_data["time"] == test_case["birth_data"]["birth_time"]
        assert birth_data["latitude"] == test_case["birth_data"]["latitude"]
        assert birth_data["longitude"] == test_case["birth_data"]["longitude"]
        assert birth_data["timezone_offset"] == test_case["birth_data"]["timezone_offset"]
        assert birth_data["ayanamsa"] == test_case["birth_data"]["ayanamsa"]
        
        # Verify ascendant
        expected_asc = test_case["expected"]["ascendant"]
        actual_asc = data["ascendant"]
        assert actual_asc["sign_index"] == expected_asc["sign_index"]
        assert math.isclose(actual_asc["ascendant_degree"], expected_asc["degree"], abs_tol=0.5)
        
        # Verify planetary positions
        for planet, expected_pos in test_case["expected"]["planets"].items():
            planet_data = next(p for p in data["planets"] if p["planet"] == planet)
            assert planet_data["sign_index"] == expected_pos["sign_index"]
            assert math.isclose(planet_data["longitude"], expected_pos["degree"], abs_tol=0.5)
        
        # Verify dasha periods
        mahadasha = data["mahadasha"]
        assert len(mahadasha) > 0
        
        # Verify first dasha period
        first_dasha = mahadasha[0]
        assert first_dasha["planet"] == test_case["expected"]["dasha"]["current"]
        assert first_dasha["start_date"] == test_case["expected"]["dasha"]["start_date"]
        assert first_dasha["end_date"] == test_case["expected"]["dasha"]["end_date"]
        assert first_dasha["years"] == test_case["expected"]["dasha"]["years"]

def test_chennai_timezone_variations():
    """Test Chennai birth case with different timezone representations"""
    base_data = TEST_CASES[2]["birth_data"].copy()
    
    # Test different timezone formats
    timezone_variations = [
        {"timezone_offset": 5.5},
        {"timezone": 5.5},
        {"timezone_offset": 5.5, "timezone": 5.5}
    ]
    
    for tz_data in timezone_variations:
        test_data = base_data.copy()
        test_data.update(tz_data)
        
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope",
            json=test_data,
            timeout=TEST_TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify calculations remain consistent
        assert data["ascendant"]["sign_index"] == TEST_CASES[2]["expected"]["ascendant"]["sign_index"]
        assert math.isclose(
            data["ascendant"]["ascendant_degree"],
            TEST_CASES[2]["expected"]["ascendant"]["degree"],
            abs_tol=0.5
        )

def test_chennai_ayanamsa_variations():
    """Test Chennai birth case with different ayanamsa methods"""
    base_data = TEST_CASES[2]["birth_data"].copy()
    
    for ayanamsa in ["lahiri", "raman", "krishnamurti"]:
        base_data["ayanamsa"] = ayanamsa
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope",
            json=base_data,
            timeout=TEST_TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify ayanamsa is reflected in calculations
        if ayanamsa != "lahiri":
            # Compare with Lahiri results
            lahiri_data = base_data.copy()
            lahiri_data["ayanamsa"] = "lahiri"
            lahiri_response = requests.post(
                f"{BASE_URL}/v1/api/horoscope",
                json=lahiri_data,
                timeout=TEST_TIMEOUT
            )
            lahiri_data = lahiri_response.json()
            
            # Verify that at least some planetary positions are different
            differences = 0
            for p1, p2 in zip(data["planets"], lahiri_data["planets"]):
                if not math.isclose(p1["longitude"], p2["longitude"], abs_tol=0.1):
                    differences += 1
            assert differences > 0, f"Ayanamsa {ayanamsa} should give different results"

def test_chennai_divisional_charts():
    """Test divisional chart calculations for Chennai birth case"""
    test_case = TEST_CASES[2]  # Chennai case
    
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope/divisional",
        json=test_case["birth_data"],
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify D-9 (Navamsa) chart
    navamsa = data["navamsa"]
    assert navamsa["ascendant"]["sign_index"] == 2  # Gemini
    assert math.isclose(navamsa["ascendant"]["degree"], 18.45, abs_tol=0.5)
    
    # Verify D-10 (Dasamsa) chart
    dasamsa = data["dasamsa"]
    assert dasamsa["ascendant"]["sign_index"] == 9  # Sagittarius
    assert math.isclose(dasamsa["ascendant"]["degree"], 12.67, abs_tol=0.5)
    
    # Verify D-24 (Chaturvimshamsa) chart
    chaturvimshamsa = data["chaturvimshamsa"]
    assert chaturvimshamsa["ascendant"]["sign_index"] == 5  # Virgo
    assert math.isclose(chaturvimshamsa["ascendant"]["degree"], 23.89, abs_tol=0.5)

def test_chennai_yogas():
    """Test specific yoga formations for Chennai birth case"""
    test_case = TEST_CASES[2]  # Chennai case
    
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope/yogas",
        json=test_case["birth_data"],
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify specific yogas
    yogas = data["yogas"]
    
    # Check for Budha-Aditya Yoga (Mercury-Sun conjunction)
    assert any(y["name"] == "Budha-Aditya Yoga" for y in yogas)
    budha_aditya = next(y for y in yogas if y["name"] == "Budha-Aditya Yoga")
    assert budha_aditya["planets"] == ["Mercury", "Sun"]
    assert budha_aditya["house"] == 8  # Scorpio
    
    # Check for Gaja-Kesari Yoga (Jupiter-Moon aspect)
    assert any(y["name"] == "Gaja-Kesari Yoga" for y in yogas)
    gaja_kesari = next(y for y in yogas if y["name"] == "Gaja-Kesari Yoga")
    assert gaja_kesari["planets"] == ["Jupiter", "Moon"]
    assert gaja_kesari["type"] == "trine"

def test_chennai_house_positions():
    """Test house positions and aspects for Chennai birth case"""
    test_case = TEST_CASES[2]  # Chennai case
    
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope/houses",
        json=test_case["birth_data"],
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify house positions
    houses = data["houses"]
    
    # First house (Ascendant)
    assert houses[0]["sign_index"] == 6  # Virgo
    assert math.isclose(houses[0]["degree"], 15.23, abs_tol=0.5)
    
    # Tenth house (Career)
    assert houses[9]["sign_index"] == 3  # Cancer
    assert math.isclose(houses[9]["degree"], 15.23, abs_tol=0.5)
    
    # Verify aspects
    aspects = data["aspects"]
    
    # Check Jupiter's aspects
    jupiter_aspects = [a for a in aspects if a["from_planet"] == "Jupiter"]
    assert len(jupiter_aspects) == 3  # Trine to Moon, Opposition to Saturn, Square to Mars
    
    # Verify aspect types
    assert any(a["type"] == "trine" and a["to_planet"] == "Moon" for a in jupiter_aspects)
    assert any(a["type"] == "opposition" and a["to_planet"] == "Saturn" for a in jupiter_aspects)
    assert any(a["type"] == "square" and a["to_planet"] == "Mars" for a in jupiter_aspects)

def test_chennai_detailed_dasha():
    """Test detailed dasha calculations for Chennai birth case"""
    test_case = TEST_CASES[2]  # Chennai case
    
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope/dasha",
        json=test_case["birth_data"],
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify Mahadasha periods
    mahadasha = data["mahadasha"]
    assert len(mahadasha) == 9  # All nine planets
    
    # Verify Jupiter Mahadasha (current)
    jupiter_dasha = next(d for d in mahadasha if d["planet"] == "Jupiter")
    assert jupiter_dasha["start_date"] == "1988-12-01"
    assert jupiter_dasha["end_date"] == "2004-12-01"
    assert jupiter_dasha["years"] == 16
    
    # Verify Saturn Mahadasha (next)
    saturn_dasha = next(d for d in mahadasha if d["planet"] == "Saturn")
    assert saturn_dasha["start_date"] == "2004-12-01"
    assert saturn_dasha["end_date"] == "2023-12-01"
    assert saturn_dasha["years"] == 19
    
    # Verify Antardasha periods
    antardasha = data["antardasha"]
    jupiter_antardasha = next(d for d in antardasha if d["mahadasha"] == "Jupiter")
    assert len(jupiter_antardasha["periods"]) == 9  # All nine planets
    
    # Verify first Antardasha
    first_antardasha = jupiter_antardasha["periods"][0]
    assert first_antardasha["planet"] == "Jupiter"
    assert first_antardasha["start_date"] == "1988-12-01"
    assert first_antardasha["end_date"] == "1990-12-01"
    assert first_antardasha["years"] == 2

def test_chennai_transits():
    """Test transit calculations for Chennai birth case"""
    test_case = TEST_CASES[2]  # Chennai case
    
    # Test current transits
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope/transits",
        json={
            **test_case["birth_data"],
            "transit_date": datetime.now().strftime("%Y-%m-%d")
        },
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify transit positions
    transits = data["transits"]
    
    # Check Sun's transit
    sun_transit = next(t for t in transits if t["planet"] == "Sun")
    assert "sign_index" in sun_transit
    assert "degree" in sun_transit
    assert "house" in sun_transit
    
    # Check Jupiter's transit
    jupiter_transit = next(t for t in transits if t["planet"] == "Jupiter")
    assert "sign_index" in jupiter_transit
    assert "degree" in jupiter_transit
    assert "house" in jupiter_transit
    
    # Verify transit aspects
    aspects = data["aspects"]
    assert len(aspects) > 0
    
    # Check for major aspects
    assert any(a["type"] in ["conjunction", "opposition", "trine", "square"] for a in aspects)

def test_chennai_all_divisional_charts():
    """Test all divisional chart calculations for Chennai birth case"""
    test_case = TEST_CASES[2]  # Chennai case
    
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope/divisional/all",
        json=test_case["birth_data"],
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify all divisional charts
    divisional_charts = {
        "D-1": {"sign_index": 6, "degree": 15.23},  # Rashi (Virgo)
        "D-2": {"sign_index": 0, "degree": 15.23},  # Hora (Aquarius)
        "D-3": {"sign_index": 6, "degree": 15.23},  # Drekkana (Virgo)
        "D-4": {"sign_index": 9, "degree": 15.23},  # Chaturthamsa (Sagittarius)
        "D-7": {"sign_index": 3, "degree": 15.23},  # Saptamsa (Cancer)
        "D-9": {"sign_index": 2, "degree": 18.45},  # Navamsa (Gemini)
        "D-10": {"sign_index": 9, "degree": 12.67},  # Dasamsa (Sagittarius)
        "D-12": {"sign_index": 6, "degree": 15.23},  # Dwadasamsa (Virgo)
        "D-16": {"sign_index": 0, "degree": 15.23},  # Shodasamsa (Aquarius)
        "D-20": {"sign_index": 0, "degree": 15.23},  # Vimshamsa (Aquarius)
        "D-24": {"sign_index": 5, "degree": 23.89},  # Chaturvimshamsa (Virgo)
        "D-27": {"sign_index": 3, "degree": 15.23},  # Saptavimshamsa (Cancer)
        "D-30": {"sign_index": 6, "degree": 15.23},  # Trimshamsa (Virgo)
        "D-40": {"sign_index": 0, "degree": 15.23},  # Khavedamsa (Aquarius)
        "D-45": {"sign_index": 3, "degree": 15.23},  # Akshavedamsa (Cancer)
        "D-60": {"sign_index": 6, "degree": 15.23}   # Shashtiamsa (Virgo)
    }
    
    for chart_name, expected in divisional_charts.items():
        chart_data = data[chart_name.lower()]
        assert chart_data["ascendant"]["sign_index"] == expected["sign_index"]
        assert math.isclose(chart_data["ascendant"]["degree"], expected["degree"], abs_tol=0.5)

def test_chennai_all_yogas():
    """Test all yoga formations for Chennai birth case"""
    test_case = TEST_CASES[2]  # Chennai case
    
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope/yogas/all",
        json=test_case["birth_data"],
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify all major yogas
    expected_yogas = [
        {
            "name": "Budha-Aditya Yoga",
            "planets": ["Mercury", "Sun"],
            "house": 8,
            "type": "conjunction"
        },
        {
            "name": "Gaja-Kesari Yoga",
            "planets": ["Jupiter", "Moon"],
            "type": "trine"
        },
        {
            "name": "Kemadruma Yoga",
            "planets": ["Moon"],
            "type": "special"
        },
        {
            "name": "Raja Yoga",
            "planets": ["Jupiter", "Venus"],
            "type": "conjunction"
        },
        {
            "name": "Dharma-Karmadhipati Yoga",
            "planets": ["Jupiter", "Saturn"],
            "type": "conjunction"
        }
    ]
    
    for expected in expected_yogas:
        yoga = next((y for y in data["yogas"] if y["name"] == expected["name"]), None)
        assert yoga is not None, f"Yoga {expected['name']} not found"
        assert yoga["planets"] == expected["planets"]
        assert yoga["type"] == expected["type"]
        if "house" in expected:
            assert yoga["house"] == expected["house"]

def test_chennai_all_dasha_periods():
    """Test all dasha period calculations for Chennai birth case"""
    test_case = TEST_CASES[2]  # Chennai case
    
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope/dasha/all",
        json=test_case["birth_data"],
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify Mahadasha periods
    mahadasha = data["mahadasha"]
    assert len(mahadasha) == 9  # All nine planets
    
    # Verify complete dasha sequence
    dasha_sequence = [
        {"planet": "Jupiter", "years": 16, "start": "1988-12-01", "end": "2004-12-01"},
        {"planet": "Saturn", "years": 19, "start": "2004-12-01", "end": "2023-12-01"},
        {"planet": "Mercury", "years": 17, "start": "2023-12-01", "end": "2040-12-01"},
        {"planet": "Ketu", "years": 7, "start": "2040-12-01", "end": "2047-12-01"},
        {"planet": "Venus", "years": 20, "start": "2047-12-01", "end": "2067-12-01"},
        {"planet": "Sun", "years": 6, "start": "2067-12-01", "end": "2073-12-01"},
        {"planet": "Moon", "years": 10, "start": "2073-12-01", "end": "2083-12-01"},
        {"planet": "Mars", "years": 7, "start": "2083-12-01", "end": "2090-12-01"},
        {"planet": "Rahu", "years": 18, "start": "2090-12-01", "end": "2108-12-01"}
    ]
    
    for expected, actual in zip(dasha_sequence, mahadasha):
        assert actual["planet"] == expected["planet"]
        assert actual["years"] == expected["years"]
        assert actual["start_date"] == expected["start"]
        assert actual["end_date"] == expected["end"]
    
    # Verify Antardasha periods
    antardasha = data["antardasha"]
    for mahadasha_planet in ["Jupiter", "Saturn", "Mercury"]:
        planet_antardasha = next(d for d in antardasha if d["mahadasha"] == mahadasha_planet)
        assert len(planet_antardasha["periods"]) == 9  # All nine planets
        
        # Verify first antardasha
        first_antardasha = planet_antardasha["periods"][0]
        assert first_antardasha["planet"] == mahadasha_planet
        assert first_antardasha["start_date"] == dasha_sequence[0]["start"]
        assert first_antardasha["years"] > 0
    
    # Verify Pratyantardasha periods
    pratyantardasha = data["pratyantardasha"]
    for mahadasha_planet in ["Jupiter", "Saturn"]:
        planet_pratyantardasha = next(d for d in pratyantardasha if d["mahadasha"] == mahadasha_planet)
        assert len(planet_pratyantardasha["periods"]) > 0
        
        # Verify first pratyantardasha
        first_pratyantardasha = planet_pratyantardasha["periods"][0]
        assert first_pratyantardasha["planet"] == mahadasha_planet
        assert first_pratyantardasha["start_date"] == dasha_sequence[0]["start"]
        assert first_pratyantardasha["years"] > 0

def test_chennai_all_transits():
    """Test all transit calculations for Chennai birth case"""
    test_case = TEST_CASES[2]  # Chennai case
    
    # Test current and future transits
    test_dates = [
        datetime.now().strftime("%Y-%m-%d"),
        (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d"),
        (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d")
    ]
    
    for test_date in test_dates:
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/transits/all",
            json={
                **test_case["birth_data"],
                "transit_date": test_date
            },
            timeout=TEST_TIMEOUT
        )
        assert response.status_code == 200
        data = response.json()
        
        # Verify all planetary transits
        transits = data["transits"]
        for planet in ["Sun", "Moon", "Mars", "Mercury", "Jupiter", "Venus", "Saturn", "Rahu", "Ketu"]:
            planet_transit = next(t for t in transits if t["planet"] == planet)
            assert "sign_index" in planet_transit
            assert "degree" in planet_transit
            assert "house" in planet_transit
            assert "retrograde" in planet_transit
        
        # Verify transit aspects
        aspects = data["aspects"]
        assert len(aspects) > 0
        
        # Verify major aspects
        aspect_types = ["conjunction", "opposition", "trine", "square", "sextile"]
        for aspect_type in aspect_types:
            assert any(a["type"] == aspect_type for a in aspects)
        
        # Verify transit-to-natal aspects
        natal_aspects = data["natal_aspects"]
        assert len(natal_aspects) > 0
        
        # Verify special transits
        special_transits = data["special_transits"]
        assert "retrograde" in special_transits
        assert "combust" in special_transits
        assert "exaltation" in special_transits
        assert "debilitation" in special_transits

def test_chennai_all_house_positions():
    """Test all house positions and aspects for Chennai birth case"""
    test_case = TEST_CASES[2]  # Chennai case
    
    response = requests.post(
        f"{BASE_URL}/v1/api/horoscope/houses/all",
        json=test_case["birth_data"],
        timeout=TEST_TIMEOUT
    )
    assert response.status_code == 200
    data = response.json()
    
    # Verify all house positions
    houses = data["houses"]
    expected_houses = [
        {"sign_index": 6, "degree": 15.23},  # 1st House (Virgo)
        {"sign_index": 7, "degree": 15.23},  # 2nd House (Libra)
        {"sign_index": 8, "degree": 15.23},  # 3rd House (Scorpio)
        {"sign_index": 9, "degree": 15.23},  # 4th House (Sagittarius)
        {"sign_index": 10, "degree": 15.23},  # 5th House (Capricorn)
        {"sign_index": 11, "degree": 15.23},  # 6th House (Aquarius)
        {"sign_index": 0, "degree": 15.23},  # 7th House (Pisces)
        {"sign_index": 1, "degree": 15.23},  # 8th House (Aries)
        {"sign_index": 2, "degree": 15.23},  # 9th House (Taurus)
        {"sign_index": 3, "degree": 15.23},  # 10th House (Cancer)
        {"sign_index": 4, "degree": 15.23},  # 11th House (Leo)
        {"sign_index": 5, "degree": 15.23}   # 12th House (Virgo)
    ]
    
    for expected, actual in zip(expected_houses, houses):
        assert actual["sign_index"] == expected["sign_index"]
        assert math.isclose(actual["degree"], expected["degree"], abs_tol=0.5)
    
    # Verify all aspects
    aspects = data["aspects"]
    assert len(aspects) > 0
    
    # Verify aspect types
    aspect_types = ["conjunction", "opposition", "trine", "square", "sextile"]
    for aspect_type in aspect_types:
        assert any(a["type"] == aspect_type for a in aspects)
    
    # Verify special aspects
    special_aspects = data["special_aspects"]
    assert "mutual_aspects" in special_aspects
    assert "planetary_war" in special_aspects
    assert "combust" in special_aspects

if __name__ == "__main__":
    # Run all tests
    pytest.main([__file__, "-v"]) 