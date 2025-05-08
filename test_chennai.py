"""
Simplified test for Chennai birth case
"""

import requests
import json
import os
import subprocess
import time
import math
from datetime import datetime, timedelta

# Test configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 10

def test_chennai_case():
    """Test specific horoscope calculations for Chennai birth case"""
    
    # Start test server
    server_process = subprocess.Popen(
        ["python", "-m", "uvicorn", "test_server:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Give it time to start
    time.sleep(2)
    
    try:
        # Chennai birth data
        birth_data = {
            "birth_date": "1988-12-01",
            "birth_time": "21:47:00",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "timezone_offset": 5.5,
            "ayanamsa": "lahiri"
        }
        
        # Expected values
        expected = {
            "ascendant": {
                "sign_index": 6,  # Virgo
                "degree": 15.23
            },
            "planets": {
                "Sun": {"sign_index": 8, "degree": 15.45},
                "Moon": {"sign_index": 3, "degree": 28.67},
                "Mars": {"sign_index": 7, "degree": 12.89},
                "Mercury": {"sign_index": 8, "degree": 23.12},
                "Jupiter": {"sign_index": 1, "degree": 18.34},
                "Venus": {"sign_index": 9, "degree": 5.56},
                "Saturn": {"sign_index": 2, "degree": 28.78},
                "Rahu": {"sign_index": 0, "degree": 15.90},
                "Ketu": {"sign_index": 6, "degree": 15.90}
            }
        }
        
        # Test the API
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope",
            json=birth_data,
            timeout=TIMEOUT
        )
        
        # Print the response for debugging
        print("API Response:", json.dumps(response.json(), indent=2))
        
        # Check status code
        assert response.status_code == 200
        data = response.json()
        
        # Verify response structure
        assert "birth_data" in data
        assert "ascendant" in data
        assert "planets" in data
        assert "mahadasha" in data
        
        # Verify birth data
        birth_data_response = data["birth_data"]
        assert birth_data_response["date"] == birth_data["birth_date"]
        assert birth_data_response["time"] == birth_data["birth_time"]
        assert birth_data_response["latitude"] == birth_data["latitude"]
        assert birth_data_response["longitude"] == birth_data["longitude"]
        assert birth_data_response["timezone_offset"] == birth_data["timezone_offset"]
        assert birth_data_response["ayanamsa"] == birth_data["ayanamsa"]
        
        # Verify ascendant
        ascendant = data["ascendant"]
        print(f"Expected ascendant: {expected['ascendant']}")
        print(f"Actual ascendant: sign_index={ascendant['sign_index']}, degree={ascendant['ascendant_degree']}")
        assert ascendant["sign_index"] == expected["ascendant"]["sign_index"]
        assert math.isclose(ascendant["ascendant_degree"], expected["ascendant"]["degree"], abs_tol=0.5)
        
        # Verify planetary positions
        for planet_obj in data["planets"]:
            planet = planet_obj["planet"]
            if planet in expected["planets"]:
                expected_pos = expected["planets"][planet]
                print(f"Planet: {planet}")
                print(f"  Expected: sign_index={expected_pos['sign_index']}, degree={expected_pos['degree']}")
                print(f"  Actual: sign_index={planet_obj['sign_index']}, longitude={planet_obj['longitude']}")
                assert planet_obj["sign_index"] == expected_pos["sign_index"]
                assert math.isclose(planet_obj["longitude"], expected_pos["degree"], abs_tol=0.5)
        
        print("All tests passed!")
        
    finally:
        # Kill the server
        server_process.terminate()
        server_process.wait()

if __name__ == "__main__":
    test_chennai_case() 