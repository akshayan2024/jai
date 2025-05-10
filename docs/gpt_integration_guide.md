# JAI API Integration Guide for Custom GPT

This guide provides detailed information for integrating the JAI (Jyotish Astrological Interpretation) API with your Custom GPT. The API provides accurate Vedic astrological calculations based on birth information.

## Overview

The JAI API allows your GPT to access powerful Vedic astrology calculations, including:

- Ascendant (Lagna) calculations
- Planetary positions with signs and houses
- Nakshatra positions
- Mahadasha (planetary period) calculations
- House positions and aspects

All these calculations are performed using the Swiss Ephemeris for astronomical accuracy.

## API Endpoints

### Primary Endpoint

```
POST /v1/api/horoscope
```

This is the main endpoint that returns a complete horoscope based on birth data.

## Request Format

The API accepts birth details in two formats:

### Preferred Method: Using Place Name

```json
{
  "birth_date": "1990-01-01",
  "birth_time": "12:30:00",
  "place": "Chennai, India",
  "ayanamsa": "lahiri"
}
```

### Alternative Method: Using Coordinates

```json
{
  "birth_date": "1990-01-01",
  "birth_time": "12:30:00",
  "latitude": 13.0827,
  "longitude": 80.2707,
  "timezone_offset": 5.5,
  "ayanamsa": "lahiri"
}
```

## Parameters Explained

| Parameter | Description | Format | Required |
|-----------|-------------|--------|----------|
| birth_date | Date of birth | YYYY-MM-DD | Yes |
| birth_time | Time of birth | HH:MM:SS (24h) | Yes |
| place | Place of birth | "City, Country" | Yes (if not using coordinates) |
| latitude | Birth latitude | Decimal degrees (-90 to 90) | Yes (if not using place) |
| longitude | Birth longitude | Decimal degrees (-180 to 180) | Yes (if not using place) |
| timezone_offset | Time zone offset from UTC | Hours (-12 to 14) | Yes (if not using place) |
| ayanamsa | Ayanamsa method | "lahiri", "raman", or "krishnamurti" | No (defaults to "lahiri") |

## Response Format

The API returns a standardized JSON response with the following structure:

```json
{
  "status": "success",
  "version": "1.0",
  "generated_at": "2023-07-01T12:34:56.789Z",
  "request_params": {
    "birth_date": "1990-01-01",
    "birth_time": "12:00:00",
    "place": "Chennai, India",
    "ayanamsa": "lahiri"
  },
  "birth_data": {
    "date": "1990-01-01",
    "time": "12:00:00",
    "place": "Chennai, India",
    "latitude": 13.0827,
    "longitude": 80.2707,
    "timezone_offset": 5.5,
    "ayanamsa": "lahiri",
    "julian_day": 2447893.0,
    "location_derived": true
  },
  "ascendant": {
    "sign": "Taurus",
    "sign_id": 2,
    "longitude": 45.23,
    "degrees": 15,
    "minutes": 13,
    "seconds": 48,
    "nakshatra": "Rohini",
    "nakshatra_id": 4,
    "nakshatra_pada": 2
  },
  "planets": [
    {
      "name": "Sun",
      "sanskrit_name": "Surya",
      "longitude": 256.83,
      "latitude": 0.0,
      "sign": "Sagittarius",
      "sign_id": 9,
      "sign_longitude": 16.83,
      "house": 8,
      "nakshatra": "Purva Ashadha",
      "nakshatra_id": 19,
      "nakshatra_pada": 3,
      "degrees": 16,
      "minutes": 49,
      "seconds": 48,
      "is_retrograde": false,
      "speed": 1.02,
      "dignity": "Neutral"
    },
    // Other planets...
  ],
  "houses": [
    {
      "house_number": 1,
      "sign": "Taurus",
      "sign_id": 2,
      "longitude": 45.23,
      "degrees": 15,
      "minutes": 13,
      "seconds": 48
    },
    // Other houses...
  ],
  "mahadasha": [
    {
      "planet": "Saturn",
      "start_date": "1990-01-01",
      "end_date": "2009-01-01",
      "years": 19
    },
    // Other periods...
  ]
}
```

## Error Handling

When an error occurs, the API returns a standardized error response:

```json
{
  "status": "error",
  "version": "1.0",
  "generated_at": "2023-07-01T12:34:56.789Z",
  "request_params": {
    "birth_date": "1990-01-01",
    "birth_time": "invalid_time",
    "place": "Chennai, India"
  },
  "error_code": "INVALID_TIME_FORMAT",
  "error_message": "The provided birth time is invalid",
  "error_details": {
    "parameter": "birth_time",
    "expected_format": "HH:MM:SS",
    "received_value": "invalid_time"
  }
}
```

## Common Error Codes

| Error Code | Description | Solution |
|------------|-------------|----------|
| INVALID_DATE_FORMAT | Invalid birth date format | Ensure date is in YYYY-MM-DD format |
| INVALID_TIME_FORMAT | Invalid birth time format | Ensure time is in HH:MM:SS format |
| GEOCODING_ERROR | Could not geocode place | Provide a valid place name or use coordinates directly |
| MISSING_LOCATION | Location information missing | Provide either place name or coordinates with timezone |
| CALCULATION_ERROR | Error during astrological calculations | Check input data or try with different parameters |

## Integrating with GPT

### Example GPT Prompt Structure

When structuring your GPT to use the JAI API, consider the following prompt patterns:

#### For Birth Chart Analysis

Prompt template:
```
Please analyze the birth chart for a person born on [DATE] at [TIME] in [PLACE].
```

GPT should:
1. Extract birth date, time, and place
2. Call the JAI API with these parameters
3. Parse the response and provide interpretations based on the astrological data

#### For Specific Questions

Prompt template:
```
What is my [PLANET/ASCENDANT/HOUSE] position if I was born on [DATE] at [TIME] in [PLACE]?
```

### Parsing Response for GPT Interpretation

Here are tips for efficiently parsing and interpreting the API response in your GPT:

1. **Planet Positions**: Use the `planets` array to access each planet's sign, house, degrees, and retrograde status
2. **Ascendant**: The `ascendant` object contains the rising sign and its exact position
3. **Houses**: The `houses` array provides each house's sign placement
4. **Mahadasha**: The `mahadasha` array shows the planetary periods, useful for timing predictions

### Error Handling in GPT

When integrating with your GPT, implement these error handling strategies:

1. Check the `status` field to determine if the request was successful
2. If `status` is "error", use the `error_message` to inform the user what went wrong
3. For validation errors, suggest the correct format based on `error_details`
4. If place geocoding fails, suggest using coordinates directly

## Astrological Interpretation Guidelines

When interpreting the API results in your GPT responses, consider these guidelines:

1. **Planets in Signs**: Each planet in a sign has specific meanings in Vedic astrology
2. **House Placements**: Planets in houses influence different areas of life
3. **Aspects**: Consider aspects between planets for deeper analysis
4. **Mahadasha Periods**: Use these for timing of events and life phases
5. **Retrograde Planets**: These have modified interpretations in Vedic astrology

## Rate Limiting

The API implements rate limiting to ensure fair usage:

- 100 requests per hour per IP address
- Exceeding this limit will result in a 429 status code

Your GPT should handle rate limit errors gracefully by informing users when limits are reached.

## Best Practices

1. Always specify all required parameters to avoid unnecessary API errors
2. Prefer using place names for easier user experience
3. Handle API errors gracefully with helpful messages
4. Cache responses when possible to avoid redundant API calls
5. Provide context with astrological interpretations, not just raw data

## Example GPT Response

When your GPT receives astrological data, structure responses like this:

```
Based on your birth details (January 1, 1990 at 12:00 PM in Chennai, India), here's your Vedic astrological chart:

Ascendant: Taurus (15°13')
  - This rising sign gives you a steady, practical approach to life

Sun: Sagittarius (16°49')
  - Positioned in the 8th house, indicating potential for transformation

Moon: Cancer (23°18')
  - In its own sign in the 3rd house, giving emotional intelligence and communication skills

Current Dasha: Saturn (until 2009-01-01)
  - A period focused on discipline, responsibility, and structure
```

## Support

For issues or questions about integrating the JAI API with your Custom GPT, please refer to the full documentation or contact support.

Happy astrological interpreting! 