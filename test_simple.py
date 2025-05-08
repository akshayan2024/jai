"""
Simple test to check API response
"""

import requests
import json

# Chennai birth data
birth_data = {
    "birth_date": "1988-12-01",
    "birth_time": "21:47:00",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone_offset": 5.5,
    "ayanamsa": "lahiri"
}

# Call the API
response = requests.post(
    "http://localhost:8000/v1/api/horoscope",
    json=birth_data,
    timeout=10
)

# Print the response
print("Status code:", response.status_code)
print("Response:", json.dumps(response.json(), indent=2))

# Print the planet data to compare
planets = response.json().get("planets", [])
for planet in planets:
    print(f"{planet['planet']}: sign_index={planet['sign_index']}, longitude={planet['longitude']}") 