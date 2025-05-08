"""
Test script for the componentized JAI API
Tests all componentized endpoints individually
"""

import requests
import json
import sys
from datetime import datetime

# Configuration
BASE_URL = "http://localhost:8000"
TIMEOUT = 10

# Chennai birth data
birth_data = {
    "birth_date": "1988-12-01",
    "birth_time": "21:47:00",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone_offset": 5.5,
    "ayanamsa": "lahiri"
}

def test_componentized_api():
    """Test all componentized endpoints"""
    print("Testing Componentized API (Make sure test_server_componentized.py is running)")
    
    try:
        # 1. Test ascendant
        print("\n=== Ascendant Component ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/ascendant",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print(json.dumps(data["ascendant"], indent=2))
        
        # 2. Test planets (D-1)
        print("\n=== Planets Component (D-1) ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/planets",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        for planet in data["planets"][:3]:  # Show first 3 planets only
            print(json.dumps(planet, indent=2))
        
        # 3. Test D-9 chart
        print("\n=== Navamsa (D-9) ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/d9",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("Ascendant:")
        print(json.dumps(data["d9"]["ascendant"], indent=2))
        print("First 2 planets:")
        print(json.dumps(data["d9"]["planets"][:2], indent=2))
        
        # 4. Test D-10 chart
        print("\n=== Dasamsa (D-10) ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/d10",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("Ascendant:")
        print(json.dumps(data["d10"]["ascendant"], indent=2))
        
        # 5. Test Mahadasha
        print("\n=== Mahadasha Component ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/mahadasha",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("First 2 Mahadasha periods:")
        print(json.dumps(data["mahadasha"][:2], indent=2))
        
        # 6. Test Antardasha
        print("\n=== Antardasha Component ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/antardasha",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("First Antardasha period:")
        print(json.dumps(data["antardasha"][0]["periods"][0], indent=2))
        
        # 7. Test Pratyantardasha
        print("\n=== Pratyantardasha Component ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/pratyantardasha",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("First Pratyantardasha period:")
        print(json.dumps(data["pratyantardasha"][0]["periods"][0], indent=2))
        
        # 8. Test House positions
        print("\n=== House Positions Component ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/houses/positions",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("First 3 Houses:")
        print(json.dumps(data["houses"][:3], indent=2))
        
        # 9. Test Aspects
        print("\n=== Aspects Component ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/aspects",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("First 2 Aspects:")
        print(json.dumps(data["aspects"][:2], indent=2))
        
        # 10. Test Yogas
        print("\n=== Yogas Component ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/yogas/individual",
            json=birth_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("First 2 Yogas:")
        print(json.dumps(data["yogas"][:2], indent=2))
        
        # 11. Test Transit positions
        print("\n=== Transit Positions Component ===")
        transit_data = birth_data.copy()
        transit_data["transit_date"] = datetime.now().strftime("%Y-%m-%d")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/transits/positions",
            json=transit_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("Transit Date:", data["transit_date"])
        print("First 2 Transit Positions:")
        print(json.dumps(data["transits"][:2], indent=2))
        
        # 12. Test Transit aspects
        print("\n=== Transit Aspects Component ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/transits/aspects",
            json=transit_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("First Transit Aspect:")
        print(json.dumps(data["aspects"][0], indent=2))
        
        # 13. Test Special transits
        print("\n=== Special Transits Component ===")
        response = requests.post(
            f"{BASE_URL}/v1/api/horoscope/transits/special",
            json=transit_data,
            timeout=TIMEOUT
        )
        print(f"Status: {response.status_code}")
        data = response.json()
        print("Special Transits:")
        print(json.dumps(data["special_transits"], indent=2))
        
        print("\n✅ All components tested successfully!")
        return True
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Connection Error: Is the server running?")
        print("Try starting it with: python -m uvicorn test_server_componentized:app --host 0.0.0.0 --port 8000")
        return False
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False

if __name__ == "__main__":
    success = test_componentized_api()
    sys.exit(0 if success else 1) 