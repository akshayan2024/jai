"""
Example demonstrating how a Custom GPT would call the JAI API and parse responses
This is a simulation of the logic a GPT would use to process astrological data
"""
import requests
import json
import re
from datetime import datetime
from typing import Dict, Any, Optional, Tuple, List

# API endpoint - change to your deployment URL
API_URL = "http://localhost:8000/v1/api/horoscope"

def extract_birth_details(user_prompt: str) -> Optional[Dict[str, str]]:
    """
    Extract birth details from a user prompt
    This simulates how a GPT would parse user input to identify date, time, and place
    """
    # Example patterns - a real GPT would use more sophisticated parsing
    date_pattern = r'(\d{4}-\d{2}-\d{2}|\d{1,2}/\d{1,2}/\d{4}|\d{1,2} [A-Za-z]+ \d{4})'
    time_pattern = r'(\d{1,2}:\d{2}(:\d{2})?( ?[APap][Mm])?)'
    place_pattern = r'(?:in|at) ([A-Za-z\s,.]+)(?:$|[.,])'
    
    # Extract date
    date_match = re.search(date_pattern, user_prompt)
    if not date_match:
        return None
    
    date_str = date_match.group(0)
    # Convert to YYYY-MM-DD if needed
    try:
        if '/' in date_str:
            parts = date_str.split('/')
            if len(parts) == 3:
                if len(parts[2]) == 4:  # MM/DD/YYYY
                    date_str = f"{parts[2]}-{parts[0].zfill(2)}-{parts[1].zfill(2)}"
                else:  # DD/MM/YYYY
                    date_str = f"{parts[2]}-{parts[1].zfill(2)}-{parts[0].zfill(2)}"
        elif ' ' in date_str and not '-' in date_str:
            # Convert "DD Month YYYY" to YYYY-MM-DD
            dt = datetime.strptime(date_str, "%d %B %Y")
            date_str = dt.strftime("%Y-%m-%d")
    except Exception:
        return None
    
    # Extract time
    time_match = re.search(time_pattern, user_prompt)
    if not time_match:
        return None
    
    time_str = time_match.group(0)
    # Convert to 24-hour format if needed
    try:
        if 'pm' in time_str.lower() or 'am' in time_str.lower():
            # Convert 12-hour format to 24-hour
            if ':' in time_str:
                time_format = "%I:%M %p" if len(time_str.split(':')[1]) <= 3 else "%I:%M:%S %p"
                dt = datetime.strptime(time_str, time_format)
                time_str = dt.strftime("%H:%M:%S")
        elif len(time_str.split(':')) == 2:
            # Add seconds if missing
            time_str = f"{time_str}:00"
    except Exception:
        return None
    
    # Extract place
    place_match = re.search(place_pattern, user_prompt)
    if not place_match:
        return None
    
    place = place_match.group(1).strip()
    
    return {
        "birth_date": date_str,
        "birth_time": time_str,
        "place": place
    }

def call_jai_api(birth_data: Dict[str, Any]) -> Dict[str, Any]:
    """Call the JAI API with birth data and return response"""
    try:
        response = requests.post(API_URL, json=birth_data, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        else:
            # Handle API errors
            error_data = response.json() if response.content else {"error": "Unknown error"}
            return {
                "status": "error",
                "error": f"API returned status code {response.status_code}",
                "details": error_data
            }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Failed to call API: {str(e)}"
        }

def interpret_ascendant(ascendant_data: Dict[str, Any]) -> str:
    """
    Generate interpretation for ascendant
    This simulates a GPT's knowledge of astrological interpretations
    """
    sign = ascendant_data["sign"]
    degrees = ascendant_data["degrees"]
    minutes = ascendant_data["minutes"]
    nakshatra = ascendant_data["nakshatra"]
    
    # Basic interpretations by sign - a real GPT would have more comprehensive knowledge
    interpretations = {
        "Aries": "You have a pioneering, courageous, and independent personality. You tend to be direct in your approach and often take initiative.",
        "Taurus": "You have a stable, practical, and determined nature. You value security and comfort, and tend to be reliable and persistent.",
        "Gemini": "You have a versatile, curious, and communicative personality. You tend to be adaptable and enjoy variety and mental stimulation.",
        "Cancer": "You have a nurturing, sensitive, and emotional nature. You value security and family, and tend to be protective and intuitive.",
        "Leo": "You have a confident, generous, and dramatic personality. You tend to be creative and seek recognition for your contributions.",
        "Virgo": "You have a practical, analytical, and detail-oriented nature. You tend to be methodical and value improvement and perfection.",
        "Libra": "You have a balanced, diplomatic, and social personality. You value harmony and relationships, and tend to be fair-minded.",
        "Scorpio": "You have an intense, resourceful, and transformative nature. You tend to be passionate and seek depth in all experiences.",
        "Sagittarius": "You have an optimistic, freedom-loving, and philosophical personality. You tend to be adventurous and seek expansion.",
        "Capricorn": "You have an ambitious, disciplined, and reserved nature. You value achievement and structure, and tend to be responsible.",
        "Aquarius": "You have an independent, humanitarian, and innovative personality. You tend to be original and value intellectual freedom.",
        "Pisces": "You have a compassionate, intuitive, and adaptable nature. You tend to be imaginative and sensitive to the feelings of others."
    }
    
    # Format the interpretation
    base_interpretation = interpretations.get(sign, "Your ascendant influences your outer personality and approach to life.")
    formatted_interpretation = f"Ascendant: {sign} at {degrees}°{minutes}'\nNakshatra: {nakshatra}\n\n{base_interpretation}"
    
    return formatted_interpretation

def interpret_planet(planet_data: Dict[str, Any]) -> str:
    """Generate interpretation for a planet position"""
    name = planet_data["name"]
    sign = planet_data["sign"]
    house = planet_data["house"]
    degrees = planet_data["degrees"]
    minutes = planet_data["minutes"]
    is_retrograde = planet_data["is_retrograde"]
    
    # Basic house meanings - a real GPT would have more comprehensive knowledge
    house_meanings = {
        1: "identity and self-image",
        2: "finances and values",
        3: "communication and siblings",
        4: "home and family",
        5: "creativity and children",
        6: "health and service",
        7: "partnerships and marriage",
        8: "transformation and shared resources",
        9: "higher learning and belief systems",
        10: "career and public status",
        11: "friends and social groups",
        12: "spirituality and hidden matters"
    }
    
    # Formatting the interpretation
    retrograde_text = " (Retrograde)" if is_retrograde else ""
    house_meaning = house_meanings.get(house, f"the {house}th house area of life")
    
    interpretation = f"{name}: {sign} at {degrees}°{minutes}'{retrograde_text}, in the {house}th house\n"
    interpretation += f"This influences your {house_meaning}."
    
    # Add retrograde interpretation if applicable
    if is_retrograde:
        interpretation += f" Since {name} is retrograde, its energy is more internalized and reflective."
    
    return interpretation

def generate_astrological_response(horoscope_data: Dict[str, Any]) -> str:
    """
    Generate a comprehensive astrological interpretation
    This simulates how a GPT would create a response based on API data
    """
    # Check if we received an error
    if horoscope_data.get("status") == "error":
        error_msg = horoscope_data.get("error_message", "Unknown error occurred")
        return f"I'm sorry, I couldn't generate your astrological chart. Error: {error_msg}"
    
    # Extract key data
    birth_data = horoscope_data.get("birth_data", {})
    ascendant = horoscope_data.get("ascendant", {})
    planets = horoscope_data.get("planets", [])
    mahadasha = horoscope_data.get("mahadasha", [])
    
    # Create the response
    response_parts = []
    
    # Introduction
    birth_place = birth_data.get("place", "")
    birth_date = birth_data.get("date", "")
    birth_time = birth_data.get("time", "")
    
    intro = f"Based on your birth details ({birth_date} at {birth_time}"
    if birth_place:
        intro += f" in {birth_place}"
    intro += "), here's your Vedic astrological chart:"
    response_parts.append(intro)
    
    # Ascendant
    response_parts.append(interpret_ascendant(ascendant))
    
    # Key planets (Sun, Moon)
    for planet in planets:
        if planet["name"] in ["Sun", "Moon"]:
            response_parts.append(interpret_planet(planet))
    
    # Current dasha period
    if mahadasha and len(mahadasha) > 0:
        current_dasha = mahadasha[0]
        response_parts.append(f"\nCurrent Dasha Period: {current_dasha['planet']} until {current_dasha['end_date']}")
        response_parts.append(f"This is a period where themes related to {current_dasha['planet']} are prominent in your life.")
    
    # Join all parts and return
    return "\n\n".join(response_parts)

def simulate_gpt_astrological_analysis(user_message: str) -> str:
    """
    Simulate how a GPT would process a user request for astrological information
    This combines all the steps: parsing input, calling API, and generating interpretation
    """
    print(f"User message: {user_message}")
    
    # Step 1: Extract birth details from user message
    birth_details = extract_birth_details(user_message)
    if not birth_details:
        return "I need your complete birth details to analyze your chart. Please provide your birth date, time, and place in this format: 'born on YYYY-MM-DD at HH:MM in City, Country'"
    
    print(f"Extracted birth details: {birth_details}")
    
    # Step 2: Call the JAI API
    api_response = call_jai_api(birth_details)
    if api_response.get("status") == "error":
        error_msg = api_response.get("error", "Unknown error")
        return f"I'm sorry, I couldn't generate your astrological chart. Error: {error_msg}"
    
    # Step 3: Generate interpretation for the user
    interpretation = generate_astrological_response(api_response)
    return interpretation

if __name__ == "__main__":
    # Example user messages
    test_messages = [
        "Can you analyze my birth chart? I was born on 1990-01-01 at 12:30 in Chennai, India.",
        "What does my horoscope say? I was born on January 15, 1985 at 8:45 PM in New York, USA.",
        "Tell me about my planets. I was born 12/25/1978 at 3:15am in London, UK."
    ]
    
    # Process each message as a GPT would
    for message in test_messages:
        print("\n" + "="*50)
        response = simulate_gpt_astrological_analysis(message)
        print("\nGPT Response:")
        print(response)
        print("="*50) 