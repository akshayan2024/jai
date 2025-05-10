# Flexible Input Format Examples for JAI API

This document demonstrates how the JAI API can handle various input formats for birth data, making it more user-friendly for integration with Custom GPTs.

## Standard JSON Input (Original Format)

```json
POST /v1/api/horoscope
{
  "birth_date": "1988-12-01",
  "birth_time": "21:47:00",
  "place": "Chennai, India",
  "ayanamsa": "lahiri"
}
```

## Flexible Input Formats (New Endpoint)

The new `/v1/api/horoscope/raw` endpoint can handle a variety of input formats:

### Example 1: Various Date Formats

```json
POST /v1/api/horoscope/raw
{
  "birth_date": "01 Dec 1988",
  "birth_time": "21:47:00",
  "place": "Chennai, India"
}
```

```json
POST /v1/api/horoscope/raw
{
  "birth_date": "Dec 01 1988",
  "birth_time": "21:47:00",
  "place": "Chennai, India"
}
```

```json
POST /v1/api/horoscope/raw
{
  "birth_date": "01-12-1988",
  "birth_time": "21:47:00",
  "place": "Chennai, India"
}
```

### Example 2: Various Time Formats

```json
POST /v1/api/horoscope/raw
{
  "birth_date": "1988-12-01",
  "birth_time": "2147",
  "place": "Chennai, India"
}
```

```json
POST /v1/api/horoscope/raw
{
  "birth_date": "1988-12-01",
  "birth_time": "21:47",
  "place": "Chennai, India"
}
```

```json
POST /v1/api/horoscope/raw
{
  "birth_date": "1988-12-01",
  "birth_time": "9:47 PM",
  "place": "Chennai, India"
}
```

### Example 3: Raw Text Format (Non-Standard JSON)

The endpoint can even handle more flexible inputs where keys or values aren't properly quoted:

```
POST /v1/api/horoscope/raw
"birth_date": 01 dec 1988,
"birth_time": "2147",
"place": "Chennai, India", 
"ayanamsa": "lahiri"
```

### Example 4: Alternative Property Names

The API also accepts alternative property names commonly used:

```json
POST /v1/api/horoscope/raw
{
  "dateOfBirth": "01 Dec 1988",
  "timeOfBirth": "9:47 PM",
  "place": "Chennai, India"
}
```

## Integration Example with Custom GPT

When a user provides birth information in a casual format, the Custom GPT can extract and send it directly to the flexible endpoint:

**User:** "Can you analyze my birth chart? I was born on Dec 1, 1988 at 9:47 in the evening in Chennai, India."

**Custom GPT (API call):**
```json
POST /v1/api/horoscope/raw
{
  "birth_date": "Dec 1, 1988",
  "birth_time": "9:47 PM",
  "place": "Chennai, India"
}
```

This approach greatly improves the user experience by handling natural language inputs without requiring strict formatting.

## Response Format

All formats return the same standardized response structure:

```json
{
  "status": "success",
  "version": "1.0",
  "generated_at": "2023-11-10T15:23:45.789Z",
  "request_params": {
    "birth_date": "1988-12-01",  // Converted to standard format
    "birth_time": "21:47:00",    // Converted to standard format
    "place": "Chennai, India",
    "ayanamsa": "lahiri"
  },
  "birth_data": {
    // Birth data details
  },
  "ascendant": {
    // Ascendant details
  },
  "planets": [
    // Planet positions
  ],
  "houses": [
    // House details
  ],
  "mahadasha": [
    // Dasha periods
  ]
}
```

## Error Handling

If the input cannot be parsed, the API returns a clear error message:

```json
{
  "status": "error",
  "version": "1.0",
  "generated_at": "2023-11-10T15:23:45.789Z",
  "error_code": "INVALID_INPUT_FORMAT",
  "error_message": "Could not parse date from 'invalid date'. Please use YYYY-MM-DD format.",
  "error_details": {
    "parameter": "birth_date",
    "received_value": "invalid date"
  }
}
``` 