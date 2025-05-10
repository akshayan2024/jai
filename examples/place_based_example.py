"""
Example demonstrating place-based birth chart calculation with JAI API
"""
import requests
import json

# API endpoint - change to your deployment URL if needed
API_URL = "http://localhost:8000/v1/api/horoscope"

def calculate_chart_with_place():
    """Calculate birth chart using place name instead of coordinates"""
    # Example birth data using place name
    birth_data = {
        "birth_date": "1990-01-01",
        "birth_time": "12:30:00",
        "place": "Chennai, India",
        "ayanamsa": "lahiri"
    }
    
    try:
        # Send request to API
        response = requests.post(API_URL, json=birth_data)
        
        # Check if request was successful
        if response.status_code == 200:
            # Parse and print response
            result = response.json()
            
            print("Birth Chart Calculated Successfully!")
            print(f"Birth Data: {birth_data['birth_date']} {birth_data['birth_time']} at {birth_data['place']}")
            
            # Print coordinates determined by the API
            print(f"\nCoordinates (automatically determined):")
            print(f"Latitude: {result['birth_data']['latitude']:.4f}")
            print(f"Longitude: {result['birth_data']['longitude']:.4f}")
            print(f"Timezone: {result['birth_data']['timezone_offset']}")
            
            # Print ascendant
            print(f"\nAscendant: {result['ascendant']['ascendant_sign_name']} "
                  f"({result['ascendant']['ascendant_degree']:.2f}°)")
            
            # Print planetary positions
            print("\nPlanetary Positions:")
            for planet in result['planets']:
                retrograde = " (R)" if planet.get('is_retrograde') else ""
                print(f"{planet['planet']:7} : {planet['sign_name']:10} {planet['degrees']:2d}°{planet['minutes']:02d}' "
                      f"(House {planet['house']}){retrograde}")
            
            # Print dasha periods
            print("\nDasha Periods:")
            for dasha in result['mahadasha']:
                print(f"{dasha['planet']:7} : {dasha['start_date']} to {dasha['end_date']} ({dasha['years']} years)")
                
            # Save result to file
            with open('chart_result.json', 'w') as f:
                json.dump(result, f, indent=2)
                print("\nFull result saved to chart_result.json")
                
        else:
            print(f"Error: {response.status_code}")
            print(response.text)
            
    except Exception as e:
        print(f"Error: {str(e)}")

if __name__ == "__main__":
    calculate_chart_with_place() 