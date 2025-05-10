# JAI API – Comprehensive Technical Specification & Requirements

## 1️⃣ Core System Constraints & Scope

### Planets List: Celestial Bodies Included

✅ **Mandatory 9 Grahas (Navagraha):**

| Index | Name     | Notes                             |
|-------|----------|-----------------------------------|
| 1     | Sun      | Surya                              |
| 2     | Moon     | Chandra                            |
| 3     | Mars     | Mangala                            |
| 4     | Mercury  | Budha                              |
| 5     | Jupiter  | Guru                               |
| 6     | Venus    | Shukra                             |
| 7     | Saturn   | Shani                              |
| 8     | Rahu     | North Lunar Node (Mean Node)       |
| 9     | Ketu     | South Lunar Node (Mean Node - 180°)|

No other celestial bodies included.

### System Fundamentals

- ✅ Uses **Whole Sign House System (W)** (fixed, no other house systems supported)
- ✅ **Constants indexed from 1 (no zero-based index)** across all constants (signs, planets, nakshatras, divisional mappings, etc.)
- ✅ Uses **Swiss Ephemeris** as backend calculation engine
- ✅ All API outputs and documentation reflect **1-based indexing**
- ✅ API clients do not configure house system or index settings (internally fixed)

### Divisional Charts Scope

✅ All divisional charts D1–D60 supported internally.
✅ API defaults: D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D60.

### Ayanamsa

✅ Default: Lahiri  
✅ Supported: Lahiri, Raman, Krishnamurti

---

## 2️⃣ Ascendant & Natal Chart Calculation

### Inputs Required

| Parameter         | Description                               |
|------------------|-------------------------------------------|
| birth_date        | Date of birth (YYYY-MM-DD)                |
| birth_time        | Time of birth (HH:MM:SS, 24h format)      |
| latitude          | Birth location latitude (decimal degrees)  |
| longitude         | Birth location longitude (decimal degrees) |
| timezone_offset   | Timezone offset from UTC (e.g. +5.5)      |

### Ascendant Calculation Flow

1. Convert birth time to **UTC**: `utc_time = birth_time - timezone_offset`
2. Compute **Julian Day (JD)** via Swiss Ephemeris `swe_julday`
3. Compute **Ascendant degree** via `swe_houses_ex(julian_day, latitude, longitude, "W")`
4. Map Ascendant degree to sign:

```
sign_index = floor(ascendant_degree / 30) + 1
```

**Formula:**

```math
ascendant_sign_index = floor(ascendant_degree / 30) + 1
```

**Python pseudocode:**

```python
def calculate_ascendant(julian_day, latitude, longitude, ayanamsa):
    swe_set_ayanamsa(ayanamsa)
    cusps, ascmc = swe_houses_ex(julian_day, latitude, longitude, 'W')
    ascendant_degree = ascmc[0]
    ascendant_sign = floor(ascendant_degree / 30) + 1
    return ascendant_degree, ascendant_sign
```

5. Return:

```json
{
  "ascendant_degree": 124.32,
  "ascendant_sign": 5,
  "ascendant_sign_name": "Leo"
}
```

### Notes

- Ascendant sign always equals **1st house**
- No cuspal house degrees (whole sign system)
- ✅ Whole Sign → ascendant sign = 1st house.

---

## 3️⃣ Natal Chart (D1) Calculation

### Per Planet:

1. Compute planetary longitude:

```python
longitude = swe_calc_ut(julian_day, planet_code, swe.FLG_SWIEPH)[0]
```

2. Map longitude to sign:

```
sign_index = floor(longitude / 30) + 1
```

3. Assign house number:

```
house_number = (sign_index - ascendant_sign_index + 12) % 12 + 1
```

**Formula:**

```math
planet_sign_index = floor(planet_longitude / 30) + 1
house_number = ((planet_sign_index - ascendant_sign + 12) % 12) + 1
```

**Python pseudocode:**

```python
def calculate_d1_planet(planet_longitude, ascendant_sign):
    sign_index = floor(planet_longitude / 30) + 1
    house = ((sign_index - ascendant_sign + 12) % 12) + 1
    return sign_index, house
```

### Output:

```json
{
  "planet": "Sun",
  "longitude": 134.55,
  "sign_index": 5,
  "sign_name": "Leo",
  "house": 1
}
```

---

## 4️⃣ Divisional Charts (D1–D60)

### Principle

Each D-n divides the 30° of a sign into `n` equal divisions. Each division maps to a derived sign based on divisional mapping.

### Per Planet:

1. Compute offset inside sign:

```
offset_in_sign = longitude % 30
```

2. Compute division number:

```
division_span = 30 / n
division_number = floor(offset_in_sign / division_span) + 1
```

3. Map division_number → divisional sign via pre-defined mapping tables

4. Assign house:

```
house_number = (div_sign_index - ascendant_sign_index + 12) % 12 + 1
```

**Formula:**

```math
division_span = 30 / n
offset_in_sign = planet_longitude % 30
division_number = floor(offset_in_sign / division_span) + 1
divisional_sign_index = divisional_mapping_table[n][planet_sign_index][division_number]
divisional_house = ((divisional_sign_index - ascendant_sign + 12) % 12) + 1
```

**Python pseudocode:**

```python
def calculate_divisional_chart(planet_longitude, ascendant_sign, n, divisional_mapping):
    sign_index = floor(planet_longitude / 30) + 1
    offset_in_sign = planet_longitude % 30
    division_span = 30 / n
    division_number = floor(offset_in_sign / division_span) + 1
    divisional_sign_index = divisional_mapping[sign_index][division_number]
    house_number = ((divisional_sign_index - ascendant_sign + 12) % 12) + 1
    return divisional_sign_index, house_number
```

✅ **divisional_mapping** → precomputed 1-based index mapping table for each D-n chart.

✅ Each D-n requires its own divisional mapping constants.

### Output Example:

```json
{
  "planet": "Sun",
  "D1": {"sign_index": 5, "sign_name": "Leo", "house": 1},
  "D9": {"sign_index": 1, "sign_name": "Aries", "house": 1},
  "D10": {"sign_index": 7, "sign_name": "Libra", "house": 3},
  ...
  "D60": {"sign_index": 12, "sign_name": "Pisces", "house": 8}
}
```

---

## 5️⃣ Vimshottari Mahadasha Calculation

### Constants

| Planet    | Years |
|-----------|-------|
| Ketu      | 7     |
| Venus     | 20    |
| Sun       | 6     |
| Moon      | 10    |
| Mars      | 7     |
| Rahu      | 18    |
| Jupiter   | 16    |
| Saturn    | 19    |
| Mercury   | 17    |

### Nakshatra → Lord Mapping

NAKSHATRA_LORDS constant maps nakshatra (1–27) → ruling planet.

### Flow

1. Compute **Moon's longitude**
2. Find **nakshatra index**:

```
nakshatra_index = floor(moon_longitude / 13.3333) + 1
```

3. Find **nakshatra lord** from NAKSHATRA_LORDS
4. Calculate **remaining percent in nakshatra**:

```
position_in_nakshatra = moon_longitude % 13.3333
elapsed_percent = (position_in_nakshatra / 13.3333) * 100
remaining_percent = 100 - elapsed_percent
```

5. Compute **remaining years in first mahadasha**:

```
remaining_years = (DASHA_YEARS[first_planet] * remaining_percent) / 100
```

6. Build mahadasha timeline: truncate first → full periods for next

### Antardasha Support

✅ Mahadasha + Antardasha calculated by default.

Optional query param `?levels=mahadasha,antardasha,pratyantardasha` for deeper levels.

### Output Example:

```json
{
  "moon": {
    "longitude": 238.2,
    "nakshatra_index": 18,
    "nakshatra_name": "Jyeshtha",
    "nakshatra_lord": "Mercury"
  },
  "vimshottari_mahadasha": [
    {"planet": "Mercury", "start_date": "1988-04-15", "end_date": "2004-08-12", "years": 16},
    {"planet": "Ketu", "start_date": "2004-08-12", "end_date": "2011-08-12", "years": 7},
    ...
  ]
}
```

---

## 6️⃣ API Endpoints & Operations

### API Endpoints

- `/api/ascendant` → Returns ascendant sign/degree (POST)
- `/api/natal-chart` → Returns ascendant + D1 placements (POST)
- `/api/divisional-chart` → Returns requested D-charts (D1–D60) (POST)
- `/api/mahadasha` → Returns Vimshottari Mahadasha timeline (POST)

### Alternative Paths

- `/api/v1/horoscope/ascendant`
- `/api/v1/horoscope/planets`
- `/api/v1/horoscope`

### Query parameters:

- `?ayanamsa=lahiri|raman|krishnamurti`

API returns JSON.

---

## 7️⃣ Error Handling

Errors return JSON:

```json
{
  "error": {
    "code": 400,
    "message": "Invalid latitude: must be between -90 and +90."
  }
}
```

Errors handled:

- Missing/invalid date, time, lat, long
- Invalid ayanamsa
- Computation failure

---

## 8️⃣ Non-Functional Requirements

- Response time:
    - Ascendant → <500ms
    - D1–D3 → <1s
    - D1–D60 → <3s
- Testing:
    - 100% constants coverage
    - 95% function coverage
    - Edge degree tests (0°, 30°, 360°)
    - Divisional boundaries (D1–D60)
    - Mahadasha balance at 0%/100%
- Deployment:
    - Python FastAPI
    - Dockerized
    - Swiss Ephemeris backend
    - No database persistence
    - `.env` config

---

## 9️⃣ Project Structure

### Constants Folder

```
/constants/
  zodiac_signs.py
  planets.py
  nakshatras.py
  divisional_mappings/d1.py ... d60.py
  nakshatra_lords.py
  dasha_years.py
```

### Services Folder

```
/services/
  ascendant_service.py
  birth_chart_service.py
  divisional_chart_service.py
  mahadasha_service.py
```

### Output Format

✅ All indices → **1-based**  
✅ Degrees → **0.0000 – 359.9999**  
✅ JSON API responses  
✅ Natural language interpretation layer → optional GPT overlay

---

## 🔟 Edge Cases in Astrological Calculations

### ✅ Calculation Edge Cases

- Ascendant exactly at **0.0°, 30.0°, 60.0°, ... 360.0°** → rounding ambiguity → must floor consistently
- Planet exactly at sign boundary → same floor() application
- Longitude = **360.0° → must clamp/modulo 0–359.999°**
- Retrograde planets → verify no effect on sign assignment (but flag in output if needed)
- Moon at **exact nakshatra boundary** → map to completed nakshatra
- Planet at division boundary in D-n → ensure correct floor() → avoid shifting division
- Last division mapping → confirm lookup covers max division index
- Non-cyclic divisional mapping systems (D27, D60) → mapping table must match correct tradition

### ✅ Implementation Edge Cases

- Swiss Ephemeris returns longitude > 360 → modulo correction
- Modulo formulas yielding 0 → must adjust +1 to maintain 1–12
- Julian Day discontinuity (pre-1582) → confirm Gregorian vs Julian correction
- Time rollover at UTC offset → ensure JD stays correct
- Overflow adding large years in Mahadasha → datetime OverflowError safeguard
- Remaining percent = 0% or 100% → must handle as valid edge without skipping
- Mahadasha first period = 0 years → still return period in response
- Planet longitude in Ketu → apply 180° shift manually from Rahu

### ✅ Domain Edge Cases

- Planets at **0° Aries** → ensure treated as valid position
- Optional divisional interpretations: retro, combust flags → clarify inclusion/exclusion
- Different classical D-n mappings (Parashara vs Jaimini) → clarify system used
- Ayanamsa variation → must apply before mapping sign
- Ascendant computation fails near polar latitudes (>±66.5°)
- Non-zodiacal longitude for custom bodies → error/fallback
- Division factor 0 or negative → block before division
- Mapping lookup missing → must fallback or error

---

## 🎉 End of Specification

This document fully specifies:

- Core system constraints and planet scope
- Calculation formulas for ascendant, natal chart, divisional charts and mahadasha
- API endpoints and operations
- Error handling schema
- Performance and deployment requirements
- Project structure and constants
- Edge cases and their handling 