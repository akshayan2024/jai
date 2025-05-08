"""
Comprehensive test script for JAI API
Tests all astrological entities with automatic server lifecycle management
"""

import requests
import json
import subprocess
import time
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 10

def start_server():
    """Start the test server"""
    print("Starting test server...")
    # Start the server process
    process = subprocess.Popen(
        ["python", "-m", "uvicorn", "test_server:app", "--host", "0.0.0.0", "--port", "8000"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    # Give it time to start
    time.sleep(3)
    return process

def stop_server(process):
    """Stop the test server"""
    print("Stopping test server...")
    process.terminate()
    process.wait(timeout=5)

def test_all():
    """Run all tests for the JAI API"""
    server_process = None
    
    try:
        # Start the server
        server_process = start_server()
        
        # Chennai birth data (test case)
        birth_data = {
            "birth_date": "1988-12-01",
            "birth_time": "21:47:00",
            "latitude": 13.0827,
            "longitude": 80.2707,
            "timezone_offset": 5.5,
            "ayanamsa": "lahiri"
        }
        
        # 1. Test health check
        print("\n=== Testing Health Check ===")
        response = requests.get(f"{BASE_URL}/v1/api/health", timeout=TIMEOUT)
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        # 2. Test root endpoint
        print("\n=== Testing Root Endpoint ===")
        response = requests.get(f"{BASE_URL}/", timeout=TIMEOUT)
        print(f"Status: {response.status_code}")
        print(json.dumps(response.json(), indent=2))
        
        # 3. Test basic horoscope (v1/api path)
        print("\n=== Testing Basic Horoscope (v1/api path) ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("Ascendant:")
        print(json.dumps(data["ascendant"], indent=2))
        print("First 3 Planets:")
        print(json.dumps(data["planets"][:3], indent=2))
        
        # 4. Test basic horoscope (api/v1 path)
        print("\n=== Testing Basic Horoscope (api/v1 path) ===")
        response = requests.post(
            f"{BASE_URL}/api/v1/horoscope",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        print("API works with both path patterns")
        
        # 5. Test divisional charts
        print("\n=== Testing Divisional Charts ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/divisional",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("Navamsa (D-9):")
        print(json.dumps(data["navamsa"], indent=2))
        
        # 6. Test all divisional charts
        print("\n=== Testing All Divisional Charts ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/divisional/all",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Available charts: {', '.join(data.keys())}")
        
        # 7. Test yogas
        print("\n=== Testing Yogas (Combinations) ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/yogas",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(json.dumps(data["yogas"], indent=2))
        
        # 8. Test all yogas
        print("\n=== Testing All Yogas ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/yogas/all",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Found {len(data['yogas'])} yoga combinations")
        
        # 9. Test house positions
        print("\n=== Testing House Positions ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/houses",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("First 3 Houses:")
        print(json.dumps(data["houses"][:3], indent=2))
        print("First 2 Aspects:")
        print(json.dumps(data["aspects"][:2], indent=2))
        
        # 10. Test all house positions
        print("\n=== Testing All House Positions ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/houses/all",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("Special Aspects:")
        print(json.dumps(data["special_aspects"], indent=2))
        
        # 11. Test dasha periods
        print("\n=== Testing Dasha Periods ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/dasha",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("First 2 Mahadasha periods:")
        print(json.dumps(data["mahadasha"][:2], indent=2))
        
        # 12. Test all dasha periods
        print("\n=== Testing All Dasha Periods ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/dasha/all",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Available dasha types: {', '.join(data.keys())}")
        
        # 13. Test transits
        print("\n=== Testing Transits ===")
        transit_data = birth_data.copy()
        transit_data["transit_date"] = datetime.now().strftime("%Y-%m-%d")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/transits",
            json=transit_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("First 3 Transit Positions:")
        print(json.dumps(data["transits"][:3], indent=2))
        
        # 14. Test all transits
        print("\n=== Testing All Transits ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/transits/all",
            json=transit_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(f"Available transit data: {', '.join(data.keys())}")
        print("Special Transits:")
        print(json.dumps(data["special_transits"], indent=2))
        
        print("\n✅ All tests completed successfully!")
        return True
        
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False
        
    finally:
        # Clean up: stop the server
        if server_process:
            stop_server(server_process)

if __name__ == "__main__":
    success = test_all()
    sys.exit(0 if success else 1) 