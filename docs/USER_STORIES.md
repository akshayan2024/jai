# JAI API User Stories

This document contains user stories for all astrological entities and features in the JAI API. These stories define the functionality from a user perspective with detailed acceptance criteria.

> *Note: This file has been reviewed and contains all 20 user stories (US-01 through US-20) with complete acceptance criteria.*

## Basic Planetary Positions

### US-01: Calculate Planetary Positions in Birth Chart

**As a** Vedic astrologer  
**I want to** retrieve the position of all 9 planets (grahas) in a birth chart  
**So that** I can interpret a person's natal chart  

**Acceptance Criteria:**
- API accepts date, time, latitude, longitude, and timezone inputs
- API returns positions for all 9 planets (Sun, Moon, Mars, Mercury, Jupiter, Venus, Saturn, Rahu, Ketu) 
- Each planet's position includes:
  - Longitude in degrees (0-360)
  - Zodiac sign (1-12)
  - Sign name
  - House position (1-12)
  - Retrograde status (true/false)
- Longitude precision is at least to 2 decimal places
- Ketu is correctly calculated as 180° from Rahu
- Ayanamsa correction is applied to all planetary positions

### US-02: Calculate Planet Positions with Different Ayanamsa

**As a** Vedic astrology researcher  
**I want to** calculate planetary positions using different ayanamsa systems  
**So that** I can compare the results and determine which system works best for my research  

**Acceptance Criteria:**
- API accepts an ayanamsa parameter with at least three options (Lahiri, Raman, Krishnamurti)
- Default ayanamsa is Lahiri if no option is specified
- All planetary positions are correctly adjusted according to the selected ayanamsa
- API returns error message if an unsupported ayanamsa is requested

### US-03: Determine Retrograde Status of Planets

**As a** Vedic astrologer  
**I want to** know which planets are retrograde in a birth chart  
**So that** I can interpret the special influence of these planets  

**Acceptance Criteria:**
- Each planet has a retrograde status flag (true/false)
- Retrograde status is determined based on the planet's speed being negative
- Retrograde status is preserved when calculating divisional charts
- Rahu and Ketu are never marked retrograde (they always move in apparent retrograde motion)
- Moon and Sun are never marked retrograde (they don't exhibit retrograde motion)

## Ascendant Calculation

### US-04: Calculate Ascendant (Lagna) for Birth Data

**As a** Vedic astrologer  
**I want to** calculate the ascendant sign and degree for a given birth data  
**So that** I can determine the rising sign and interpret the chart accordingly  

**Acceptance Criteria:**
- API accepts date, time, latitude, longitude, and timezone inputs
- API returns ascendant degree (0-360)
- API returns ascendant sign index (1-12)
- API returns ascendant sign name
- Ascendant calculation takes into account the exact time and geographic location
- Ayanamsa correction is applied to the ascendant position

### US-05: Calculate Whole Sign Houses from Ascendant

**As a** Vedic astrologer  
**I want to** get the house positions for all planets based on the Whole Sign house system  
**So that** I can interpret planetary influences in different areas of life  

**Acceptance Criteria:**
- House 1 is assigned to the sign of the ascendant
- Houses 2-12 follow in zodiacal order from the ascendant
- Each planet is assigned to a house based on its sign
- House positions are integers from 1 to 12
- House positions are included in all chart calculations

## Divisional Charts

### US-06: Generate Divisional Chart D9 (Navamsa)

**As a** Vedic astrologer  
**I want to** calculate the D9 (Navamsa) divisional chart for a birth time  
**So that** I can analyze deeper karmic patterns and marriage indications  

**Acceptance Criteria:**
- API accepts natal planetary positions and ascendant as input
- API correctly divides each sign into 9 equal parts (3°20' each)
- API maps each division to the correct sign according to classical Navamsa mapping
- API returns positions of all 9 planets in the D9 chart
- Each planet position includes divisional sign index, sign name, and house position
- Retrograde status is preserved from the natal chart
- D9 chart houses are calculated based on the D9 ascendant

### US-07: Generate Multiple Divisional Charts

**As a** Vedic astrologer  
**I want to** generate multiple divisional charts (D1-D60) from a single birth data  
**So that** I can analyze different aspects of a person's life  

**Acceptance Criteria:**
- API accepts a list of requested divisional charts (e.g., "D1,D9,D12")
- API returns the specified divisional charts in a structured format
- Each divisional chart contains all 9 planets with their respective positions
- API returns appropriate error message if an unsupported divisional chart is requested
- At minimum, D1, D9, and D12 charts are supported
- Each chart is calculated according to classical divisional mapping rules

### US-08: Calculate Planets in Specific Divisional Chart

**As a** Vedic astrologer  
**I want to** view planetary positions in a specific divisional chart  
**So that** I can focus on particular life aspects represented by that chart  

**Acceptance Criteria:**
- API accepts birth data and divisional chart number as input
- API returns all planetary positions for that specific divisional chart
- API includes divisional chart ascendant
- Positions include sign, house, and retrograde status
- API provides error message if the requested divisional chart is not supported
- Results include mapping information specific to the divisional chart

## Nakshatra Calculations

### US-09: Determine Nakshatra Position of the Moon

**As a** Vedic astrologer  
**I want to** determine the Moon's nakshatra (lunar mansion) in a birth chart  
**So that** I can interpret more detailed lunar influences and determine the starting Mahadasha  

**Acceptance Criteria:**
- API calculates the Moon's nakshatra based on its longitude
- API returns nakshatra index (1-27)
- API returns nakshatra name
- API returns nakshatra lord (ruling planet)
- API returns pada (quarter, 1-4) within the nakshatra
- Nakshatra calculation accounts for the selected ayanamsa

### US-10: Calculate Nakshatra Positions for All Planets

**As a** Vedic astrologer  
**I want to** know the nakshatra position of each planet  
**So that** I can interpret subtle planetary influences  

**Acceptance Criteria:**
- API returns nakshatra position for each of the 9 planets
- Each nakshatra position includes nakshatra index, name, lord, and pada
- Nakshatra spans are accurately calculated (each spans 13°20')
- Nakshatra positions account for the selected ayanamsa
- Pada (quarter) within nakshatra is correctly calculated
- Results include degrees traversed within the nakshatra

## Mahadasha Calculations

### US-11: Calculate Vimshottari Mahadasha Periods

**As a** Vedic astrologer  
**I want to** calculate the Vimshottari Mahadasha periods for a person  
**So that** I can analyze major planetary influences throughout their life  

**Acceptance Criteria:**
- API accepts birth date, time, location data as input
- API determines Moon's nakshatra at birth
- API calculates current mahadasha (ruling planet) based on Moon's nakshatra
- API returns ordered sequence of all 9 mahadashas with start and end dates
- API correctly calculates the balance of the first mahadasha at birth
- Each mahadasha period has the appropriate duration (Sun: 6 years, Moon: 10 years, etc.)
- Total mahadasha cycle equals 120 years

### US-12: Calculate Antardasha (Sub-periods) within Mahadasha

**As a** Vedic astrologer  
**I want to** calculate antardasha (sub-periods) within each mahadasha  
**So that** I can analyze more detailed planetary influences  

**Acceptance Criteria:**
- API returns all antardashas within each mahadasha period
- Antardashas follow the standard Vimshottari sequence starting with the mahadasha lord
- Each antardasha duration is proportional to the planetary dasha years
- Start and end dates for each antardasha are accurate
- All antardashas within a mahadasha exactly span the complete mahadasha period
- The first antardasha in each mahadasha is always ruled by the mahadasha planet

### US-13: Calculate Current Mahadasha and Balance

**As a** Vedic astrologer  
**I want to** know a person's current mahadasha and its remaining duration  
**So that** I can provide timely predictions  

**Acceptance Criteria:**
- API identifies the currently active mahadasha based on birth data and current date
- API returns the ruling planet of the current mahadasha
- API returns start and end dates of the current mahadasha
- API calculates and returns the exact balance of the current mahadasha in years/months/days
- API identifies current antardasha within the mahadasha
- API returns the ruling planet of the current antardasha with its remaining duration

## Special Chart Features

### US-14: Detect Planetary Aspects

**As a** Vedic astrologer  
**I want to** identify classical Vedic aspects between planets  
**So that** I can interpret planetary relationships and influences  

**Acceptance Criteria:**
- API calculates aspects according to classical Vedic rules (not Western aspects)
- Each planet aspects its 7th house (180°) from its position
- Mars, Jupiter, and Saturn have special aspects (Mars: 4th & 8th; Jupiter: 5th & 9th; Saturn: 3rd & 10th)
- API returns a list of all planetary aspects in the chart
- Each aspect entry identifies the aspecting planet, the aspected planet or house, and the aspect type
- Aspect strength/completeness is calculated based on orb/distance

### US-15: Calculate Planetary Strengths (Shadbala)

**As a** Vedic astrologer  
**I want to** calculate the relative strengths of planets in a chart  
**So that** I can determine which planets will manifest their results most prominently  

**Acceptance Criteria:**
- API calculates at least 3 different strength factors for each planet
- API includes positional strength (Sthana Bala)
- API includes directional strength (Dig Bala)
- API includes temporal strength (Kala Bala)
- API calculates total strength (Shadbala) by combining individual strengths
- Results include normalized strength scores (percentage or 0-1 scale)
- Results indicate whether each planet is strong, moderate, or weak

### US-16: Identify Planetary Combinations (Yogas)

**As a** Vedic astrologer  
**I want to** identify important planetary combinations (yogas) in a birth chart  
**So that** I can interpret their specific influences  

**Acceptance Criteria:**
- API identifies at least 15 major classical yogas
- Each yoga identification includes the name of the yoga and the participating planets
- API provides a brief description of the signification/effect of each yoga
- API categorizes yogas (e.g., wealth yogas, spiritual yogas, etc.)
- API indicates the strength/completeness of each yoga
- Results exclude yogas that are technically formed but too weak to manifest

## Chart Analysis and Interpretation

### US-17: Generate Basic Chart Interpretation

**As a** Vedic astrology enthusiast  
**I want to** get a basic textual interpretation of a birth chart  
**So that** I can understand the general astrological influences  

**Acceptance Criteria:**
- API generates paragraph descriptions for at least 5 major chart components
- Interpretation includes ascendant sign characteristics
- Interpretation includes key planet placements and their effects
- Interpretation includes major planetary combinations (yogas)
- Text is grammatically correct and coherent
- Interpretation avoids overly negative or deterministic language
- Output distinguishes between strong and weak planetary influences

### US-18: Calculate Compatibility Between Two Charts

**As a** relationship astrologer  
**I want to** calculate astrological compatibility between two birth charts  
**So that** I can assess relationship potential  

**Acceptance Criteria:**
- API accepts birth data for two individuals
- API calculates Vedic compatibility metrics (minimum of 8 Kuta points)
- API returns an overall compatibility score (percentage or 0-10 scale)
- API provides scores for different relationship factors (e.g., temperament, longevity, etc.)
- Results include the Moon sign compatibility (Rashi Kuta)
- Results include the nakshatra compatibility (Nakshatra Kuta)
- API returns textual interpretation of compatibility strengths and challenges

## API Infrastructure

### US-19: Validate Input Data

**As a** developer integrating with the JAI API  
**I want to** receive clear validation feedback for input data  
**So that** I can correct errors before processing  

**Acceptance Criteria:**
- API validates date format (YYYY-MM-DD)
- API validates time format (HH:MM:SS)
- API validates latitude range (-90 to +90)
- API validates longitude range (-180 to +180)
- API validates timezone offset (-12 to +14)
- API returns specific error messages identifying invalid parameters
- Error responses include the expected format/range for each parameter
- API performs validation before any calculation logic

### US-20: Access API Documentation

**As a** developer integrating with the JAI API  
**I want to** access comprehensive API documentation  
**So that** I can understand how to use the API correctly  

**Acceptance Criteria:**
- API provides Swagger/OpenAPI documentation at /v1/docs endpoint
- Documentation includes all available endpoints
- Each endpoint documentation includes required and optional parameters
- Documentation shows example requests and responses
- Documentation includes error response formats
- Documentation provides authentication information (if applicable)
- Documentation is accessible through a web browser 