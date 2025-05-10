# Integrating JAI API with OpenAI Custom GPT

This guide provides detailed instructions for integrating the JAI (Jyotish Astrological Interpretation) API with a Custom GPT on the OpenAI platform.

## Overview

By integrating the JAI API with your Custom GPT, you can create an astrological assistant that provides accurate Vedic astrological calculations and interpretations based on birth information.

## Step 1: Create a New Custom GPT

1. Navigate to ChatGPT (https://chat.openai.com/)
2. Click on "Explore" or "Create" to start creating a new Custom GPT
3. Provide a name and description for your GPT (e.g., "Vedic Astrology Advisor")

## Step 2: Configure the Custom GPT

### Instructions Section

Add these instructions to teach your GPT about its capabilities:

```
You are a Vedic Astrology advisor with access to precise astronomical calculations. You can analyze birth charts based on a person's birth date, time, and place.

When a user asks questions about their birth chart or requests an astrological reading:
1. Extract the birth date, time, and location from their question
2. If any information is missing, politely ask for the complete birth details
3. Use the JAI API to calculate precise planetary positions and astrological data
4. Provide interpretations based on Vedic astrology principles
5. Explain the results in a clear, insightful manner
6. Focus on the specific area the user is asking about (career, relationships, etc.)

Present birth chart information in a clear, organized format. Include:
- Ascendant (rising sign) with degrees and nakshatra
- Key planetary positions with their signs, houses, degrees, and nakshatras
- Current dasha (planetary period) information
- Yogas or special planetary combinations when relevant

Use proper Vedic astrology terminology but explain concepts in accessible language.
```

## Step 3: Create an Action with OpenAPI Schema

In the "Actions" section, add a new action with the following details:

### Authentication

Choose the appropriate authentication method:
- For development/testing: "None" (if your API is publicly accessible)
- For production: "API Key" (recommended for security)

If using API Key:
- Auth Type: API Key
- Auth Location: Header
- Key Name: `x-api-key`

### OpenAPI Schema

Copy and paste the following OpenAPI Schema that defines our JAI API:

```yaml
openapi: 3.0.0
info:
  title: JAI (Jyotish Astrological Interpretation) API
  description: API for Vedic astrology calculations providing planetary positions, ascendant, houses, and dasha periods based on birth details
  version: 1.0.0
servers:
  - url: https://your-api-endpoint.com
    description: JAI API Server
paths:
  /v1/api/horoscope:
    post:
      operationId: generateHoroscope
      summary: Generate a Vedic horoscope based on birth details
      description: |
        Calculate a complete Vedic astrological chart including ascendant, planetary positions, houses, and dasha periods using the Swiss Ephemeris.
        
        You can provide birth location using either place name (preferred) or explicit coordinates with timezone.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - birth_date
                - birth_time
              properties:
                birth_date:
                  type: string
                  description: Date of birth in YYYY-MM-DD format
                  example: "1990-01-01"
                birth_time:
                  type: string
                  description: Time of birth in HH:MM:SS format (24h)
                  example: "12:30:00"
                place:
                  type: string
                  description: Place of birth (city, country) - preferred method
                  example: "Chennai, India"
                latitude:
                  type: number
                  description: Birth latitude (-90 to 90 degrees) - alternative to place
                  minimum: -90
                  maximum: 90
                  example: 13.0827
                longitude:
                  type: number
                  description: Birth longitude (-180 to 180 degrees) - alternative to place
                  minimum: -180
                  maximum: 180
                  example: 80.2707
                timezone_offset:
                  type: number
                  description: Timezone offset from UTC in hours - alternative to place
                  minimum: -12
                  maximum: 14
                  example: 5.5
                ayanamsa:
                  type: string
                  description: Ayanamsa method to use for calculations
                  enum: [lahiri, raman, krishnamurti]
                  default: lahiri
                  example: "lahiri"
      responses:
        '200':
          description: Successful horoscope calculation
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "success"
                  version:
                    type: string
                    example: "1.0"
                  generated_at:
                    type: string
                    format: date-time
                    example: "2023-07-01T12:34:56.789Z"
                  request_params:
                    type: object
                    example:
                      birth_date: "1990-01-01"
                      birth_time: "12:00:00"
                      place: "Chennai, India"
                      ayanamsa: "lahiri"
                  birth_data:
                    type: object
                    properties:
                      date:
                        type: string
                        example: "1990-01-01"
                      time:
                        type: string
                        example: "12:00:00"
                      place:
                        type: string
                        example: "Chennai, India"
                      latitude:
                        type: number
                        example: 13.0827
                      longitude:
                        type: number
                        example: 80.2707
                      timezone_offset:
                        type: number
                        example: 5.5
                      ayanamsa:
                        type: string
                        example: "lahiri"
                      julian_day:
                        type: number
                        example: 2447893.0
                      location_derived:
                        type: boolean
                        example: true
                  ascendant:
                    type: object
                    properties:
                      sign:
                        type: string
                        example: "Taurus"
                      sign_id:
                        type: integer
                        example: 2
                      longitude:
                        type: number
                        example: 45.23
                      degrees:
                        type: integer
                        example: 15
                      minutes:
                        type: integer
                        example: 13
                      seconds:
                        type: integer
                        example: 48
                      nakshatra:
                        type: string
                        example: "Rohini"
                      nakshatra_id:
                        type: integer
                        example: 4
                      nakshatra_pada:
                        type: integer
                        example: 2
                  planets:
                    type: array
                    items:
                      type: object
                      properties:
                        name:
                          type: string
                          example: "Sun"
                        sanskrit_name:
                          type: string
                          example: "Surya"
                        longitude:
                          type: number
                          example: 256.83
                        latitude:
                          type: number
                          example: 0.0
                        sign:
                          type: string
                          example: "Sagittarius"
                        sign_id:
                          type: integer
                          example: 9
                        sign_longitude:
                          type: number
                          example: 16.83
                        house:
                          type: integer
                          example: 8
                        nakshatra:
                          type: string
                          example: "Purva Ashadha"
                        nakshatra_id:
                          type: integer
                          example: 19
                        nakshatra_pada:
                          type: integer
                          example: 3
                        degrees:
                          type: integer
                          example: 16
                        minutes:
                          type: integer
                          example: 49
                        seconds:
                          type: integer
                          example: 48
                        is_retrograde:
                          type: boolean
                          example: false
                        speed:
                          type: number
                          example: 1.02
                        dignity:
                          type: string
                          example: "Neutral"
                  houses:
                    type: array
                    items:
                      type: object
                      properties:
                        house_number:
                          type: integer
                          example: 1
                        sign:
                          type: string
                          example: "Taurus"
                        sign_id:
                          type: integer
                          example: 2
                        longitude:
                          type: number
                          example: 45.23
                        degrees:
                          type: integer
                          example: 15
                        minutes:
                          type: integer
                          example: 13
                        seconds:
                          type: integer
                          example: 48
                  mahadasha:
                    type: array
                    items:
                      type: object
                      properties:
                        planet:
                          type: string
                          example: "Saturn"
                        start_date:
                          type: string
                          example: "1990-01-01"
                        end_date:
                          type: string
                          example: "2009-01-01"
                        years:
                          type: number
                          example: 19
        '400':
          description: Invalid request parameters
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "error"
                  version:
                    type: string
                    example: "1.0"
                  generated_at:
                    type: string
                    format: date-time
                    example: "2023-07-01T12:34:56.789Z"
                  request_params:
                    type: object
                    example:
                      birth_date: "1990-01-01"
                      birth_time: "invalid_time"
                      place: "Chennai, India"
                  error_code:
                    type: string
                    example: "INVALID_TIME_FORMAT"
                  error_message:
                    type: string
                    example: "The provided birth time is invalid"
                  error_details:
                    type: object
                    example:
                      parameter: "birth_time"
                      expected_format: "HH:MM:SS"
                      received_value: "invalid_time"
        '429':
          description: Rate limit exceeded
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "error"
                  error_code:
                    type: string
                    example: "RATE_LIMIT_EXCEEDED"
                  error_message:
                    type: string
                    example: "Rate limit exceeded. Please try again later."
  /v1/api/horoscope/raw:
    post:
      operationId: generateHoroscopeRaw
      summary: Generate a Vedic horoscope from flexible, user-friendly input formats
      description: |
        Calculate a complete Vedic astrological chart with flexible input format support.
        
        This endpoint is designed to be more forgiving with input formats, supporting various date and time formats.
        It's especially useful for Custom GPT integration where users might provide birth information in less structured ways.
        
        You can provide birth location using either place name (preferred) or explicit coordinates with timezone.
      requestBody:
        required: true
        content:
          application/json:
            schema:
              type: object
              required:
                - birth_date
                - birth_time
              properties:
                birth_date:
                  type: string
                  description: |
                    Date of birth in various formats:
                    - YYYY-MM-DD (1990-01-01)
                    - DD-MM-YYYY (01-01-1990)
                    - DD MMM YYYY (01 Jan 1990)
                    - MMM DD YYYY (Jan 01 1990)
                  example: "01 Dec 1988"
                birth_time:
                  type: string
                  description: |
                    Time of birth in various formats:
                    - HH:MM:SS (13:30:00)
                    - HH:MM (13:30)
                    - HHMM (1330)
                    - With AM/PM (1:30 PM)
                  example: "2147"
                place:
                  type: string
                  description: Place of birth (city, country) - preferred method
                  example: "Chennai, India"
                latitude:
                  type: number
                  description: Birth latitude (-90 to 90 degrees) - alternative to place
                  minimum: -90
                  maximum: 90
                  example: 13.0827
                longitude:
                  type: number
                  description: Birth longitude (-180 to 180 degrees) - alternative to place
                  minimum: -180
                  maximum: 180
                  example: 80.2707
                timezone_offset:
                  type: number
                  description: Timezone offset from UTC in hours - alternative to place
                  minimum: -12
                  maximum: 14
                  example: 5.5
                ayanamsa:
                  type: string
                  description: Ayanamsa method to use for calculations
                  enum: [lahiri, raman, krishnamurti]
                  default: lahiri
                  example: "lahiri"
            examples:
              standard:
                summary: Standard format
                value: {
                  "birth_date": "1988-12-01",
                  "birth_time": "21:47:00",
                  "place": "Chennai, India",
                  "ayanamsa": "lahiri"
                }
              flexible:
                summary: Flexible format
                value: {
                  "birth_date": "01 Dec 1988",
                  "birth_time": "2147",
                  "place": "Chennai, India",
                  "ayanamsa": "lahiri"
                }
              raw:
                summary: Raw format
                value: '"birth_date": 01 dec 1988, "birth_time": "2147", "place": "Chennai, India", "ayanamsa": "lahiri"'
          text/plain:
            schema:
              type: string
              example: '"birth_date": 01 dec 1988, "birth_time": "2147", "place": "Chennai, India", "ayanamsa": "lahiri"'
      responses:
        '200':
          description: Successful horoscope calculation
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/HoroscopeResponse'
        '400':
          description: Invalid input format or missing required data
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "error"
                  version:
                    type: string
                    example: "1.0"
                  generated_at:
                    type: string
                    format: date-time
                    example: "2023-07-01T12:34:56.789Z"
                  error_code:
                    type: string
                    example: "INVALID_INPUT_FORMAT"
                  error_message:
                    type: string
                    example: "Could not parse input: Invalid date format"
        '429':
          description: Rate limit exceeded
          content:
            application/json:
              schema:
                type: object
                properties:
                  status:
                    type: string
                    example: "error"
                  error_code:
                    type: string
                    example: "RATE_LIMIT_EXCEEDED"
                  error_message:
                    type: string
                    example: "Rate limit exceeded. Please try again later."

## Step 4: Add Example Conversations

In the "Example conversations" section, add examples showing how your Custom GPT should interact with users:

### Example 1: Basic Birth Chart Analysis

**User:** Can you analyze my birth chart? I was born on January 1, 1990 at 12:30 PM in Chennai, India.

**GPT:**
*I'll analyze your Vedic birth chart based on these details:*

*First, let me calculate your precise planetary positions using the JAI API...*

*Based on your birth details (January 1, 1990 at 12:30 PM in Chennai, India), here's your Vedic astrological chart:*

*Ascendant: Taurus (15°13′) in Rohini Nakshatra*
*This gives you a stable, patient, and determined personality. You likely approach life in a practical, methodical way and value security and comfort.*

*Sun: Sagittarius (16°49′) in the 8th house*
*With your Sun in Sagittarius, you have an optimistic, freedom-loving nature. Positioned in the 8th house, this indicates a deep interest in mysteries, transformation, and hidden knowledge.*

*Moon: Cancer (23°18′) in the 3rd house*
*Your Moon in its own sign of Cancer makes you emotionally sensitive and nurturing. In the 3rd house, this enhances your communication skills and connection with siblings or close friends.*

*Your current Mahadasha (planetary period) is Saturn until 2009, followed by Mercury.*
*This Saturn period brings focus on discipline, responsibility, and long-term achievements.*

*Would you like me to explore a specific area of your chart in more detail?*

### Example 2: Specific Question About Career

**User:** What does my birth chart say about my career? I was born on May 15, 1985 at 8:45 AM in New York.

**GPT:**
*To provide accurate career insights from your Vedic birth chart, I need to calculate your planetary positions using your birth details.*

*Analyzing your birth data (May 15, 1985 at 8:45 AM in New York)...*

*Based on your Vedic birth chart, here's what I can tell you about your career:*

*Your 10th house of career is in Pisces, with Jupiter (the ruler of Pisces) placed in the 11th house of gains and aspirations. This suggests a career that involves creativity, compassion, or helping others. You may excel in fields related to healthcare, counseling, art, music, or spiritual work.*

*Saturn aspects your 10th house, indicating that you build your career slowly but steadily, with discipline and perseverance. You're likely to achieve greater success in the latter part of your life.*

*Your 10th lord Jupiter in the 11th house suggests that networking and social connections play an important role in your professional growth. You may find success in large organizations or institutions where you can use your humanitarian values.*

*Mercury in the 9th house indicates potential success in teaching, publishing, consulting, or international business. You have the ability to communicate complex ideas effectively.*

*Would you like more specific insights about potential career paths or timing of career events?*

## Step 5: Configure Conversation Starters

Add these conversation starters to help users begin interacting with your GPT:

1. "Can you analyze my birth chart? I was born on January 1, 1990 at 12:30 PM in Chennai, India."
2. "What does my chart say about my career potential? I was born on June 15, 1988 at 9:30 AM in London."
3. "When will I find a relationship? My birth details are July 23, 1992, 3:15 PM in Sydney, Australia."
4. "What are my strengths and weaknesses according to Vedic astrology? Born December 5, 1983 at 7:45 AM in Toronto."
5. "Can you tell me about my current dasha period? Born August 12, 1976 at 10:20 PM in Chicago."

## Step 6: Test Your Custom GPT

After setting up your Custom GPT:

1. Test it with various birth details to ensure it correctly extracts date, time, and location
2. Verify it properly calls the JAI API and presents the information clearly
3. Make any necessary adjustments to the instructions to improve responses

## Best Practices for Your Astrological Custom GPT

### Input Handling

Train your GPT to handle various date and time formats:
- "January 1, 1990" or "1990-01-01" or "01/01/1990"
- "3:30 PM" or "15:30" or "15:30:00"
- Place names with or without country

### Output Formatting

Instruct your GPT to:
- Present important chart factors first (ascendant, sun, moon positions)
- Format degrees with proper symbols (e.g., 15°13′)
- Group information logically (personal planets, outer planets, etc.)
- Explain technical terms when they're first used

### Interpretation Guidelines

For accurate astrological interpretations:
- Focus on the most significant chart factors
- Consider aspect relationships between planets
- Acknowledge the complexity of chart analysis
- Provide balanced interpretations that include both potential strengths and challenges
- Avoid overly deterministic or fatalistic predictions

## Troubleshooting

### Common Issues

1. **Missing Birth Details**: If the GPT fails to request missing information, adjust the instructions to emphasize the importance of complete birth data.

2. **API Connection Errors**: If your GPT can't connect to the JAI API:
   - Verify your API endpoint is correct and accessible
   - Check authentication settings
   - Ensure your API server is running

3. **Interpretation Quality**: If interpretations are too generic:
   - Enhance the GPT instructions with more specific guidance
   - Add more detailed examples of quality interpretations
   - Include more Vedic astrology reference information

## Support and Resources

If you need help integrating the JAI API with your Custom GPT, please contact our support team at [support@your-domain.com].

For more information on Vedic astrology principles, refer to the following resources:
- [Link to your documentation]
- [Link to Vedic astrology reference] 