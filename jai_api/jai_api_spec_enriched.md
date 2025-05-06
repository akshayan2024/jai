
# JAI API – Full Technical Specification & Deployment Plan

## 1️⃣ Planets List: Celestial Bodies Included

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

✅ No other celestial bodies included.

---

## 2️⃣ Divisional Charts Scope

✅ All divisional charts D1–D60 supported internally.

✅ API defaults: D1, D2, D3, D4, D7, D9, D10, D12, D16, D20, D24, D27, D30, D60.

✅ Each chart uses **predefined classical divisional mapping constants.**

✅ **All mappings must be validated against Parashara Hora Shastra or equivalent classical texts.**

✅ Each mapping is implemented as a nested dictionary:

```python
divisional_mapping[D_n][sign_index][division_number] = mapped_sign_index
```

Example for D3:

| Sign | Div1 | Div2 | Div3 |
|------|------|------|------|
| 1    | 1    | 5    | 9    |
| 2    | 2    | 6    | 10   |
| 3    | 3    | 7    | 11   |
| …    | …    | …    | …    |

✅ Similar tables implemented for D2–D60.

✅ If mapping not implemented → API returns:

```json
{ "error": { "code": 500, "message": "Divisional mapping for D27 is not implemented." } }
```

✅ Mappings stored in `/constants/divisional_mappings/` as Python files or JSON.

✅ Mappings loaded at app startup and cached.

---

## 3️⃣ Retrograde Handling

✅ Retrograde flag computed per planet using Swiss Ephemeris speed:

```python
is_retrograde = speed < 0.0
```

✅ Flag included in **all output charts (D1–D60)**.

Example response for `/api/natal-chart`:

```json
{
  "planet": "Saturn",
  "longitude": 285.23,
  "sign_index": 10,
  "sign_name": "Capricorn",
  "house": 6,
  "is_retrograde": true
}
```

✅ Flag preserved across divisional charts:

```json
{
  "planet": "Saturn",
  "divisional_sign_index": 4,
  "divisional_sign_name": "Cancer",
  "divisional_house": 10,
  "is_retrograde": true
}
```

✅ Retrograde status stays same across D1–D60 (birth-time based).

✅ Mandatory inclusion in all API responses.

---

## 4️⃣ API Operations

✅ Endpoints use `/v1/` prefix.

| Endpoint                     | Description                         |
|-----------------------------|------------------------------------|
| /v1/api/ascendant            | Returns ascendant sign/degree       |
| /v1/api/natal-chart          | Returns D1 natal chart              |
| /v1/api/divisional-chart     | Returns requested D1–D60 charts     |
| /v1/api/mahadasha            | Returns Vimshottari Mahadasha       |

✅ Query parameters:

- `?ayanamsa=lahiri|raman|krishnamurti`
- `?charts=D1,D9,D10,D60`

✅ API returns JSON.

✅ FastAPI `/docs` enabled → OpenAPI auto-generated → accessible at `/v1/docs`.

✅ No rate limiting at this stage.

✅ Render logs will capture stdout/stderr logs → `logger.info()` suffices.

---

## 5️⃣ Error Handling

✅ JSON error structure:

```json
{
  "error": {
    "code": 400,
    "message": "Invalid latitude: must be between -90 and +90."
  }
}
```

✅ Errors include:

| Error Type            | Example Message                                  |
|---------------------|--------------------------------------------------|
| Missing parameter     | "Missing parameter: birth_date"                  |
| Invalid date          | "Invalid date format: YYYY-MM-DD"                |
| Invalid time          | "Invalid time format: HH:MM:SS"                  |
| Invalid latitude      | "Invalid latitude: must be between -90 and +90." |
| Unknown ayanamsa      | "Unsupported ayanamsa: allowed values are…"      |
| Mapping not found     | "Divisional mapping for D27 not implemented."    |

✅ 400 for validation errors; 500 for internal computation errors.

---

## 6️⃣ Input Validation

✅ Fields:

| Field            | Validation                         |
|-----------------|------------------------------------|
| birth_date       | ISO 8601 date YYYY-MM-DD           |
| birth_time       | 24h HH:MM:SS                       |
| latitude         | -90.0 ≤ latitude ≤ +90.0           |
| longitude        | -180.0 ≤ longitude ≤ +180.0        |
| timezone_offset  | -12 ≤ offset ≤ +14                 |
| ayanamsa         | lahiri, raman, krishnamurti        |

✅ Invalid → return structured JSON error.

✅ No silent fallback on bad input.

---

## 7️⃣ Non-Functional Requirements

✅ Performance:

| Operation                  | Target Response Time |
|---------------------------|--------------------|
| Ascendant                  | < 500 ms           |
| D1 + 1–2 charts            | < 1 sec            |
| D1–D60 + mahadasha         | < 3 sec            |

✅ Testing:

- 100% constants coverage
- 95% function coverage
- Edge tests at 0°, 30°, 60°, 90°, 360°
- Divisional boundaries per D1–D60
- Mahadasha balance 0% / 100%
- Stress test: 1000 parallel requests

✅ Deployment:

- Hosted on **Render.com**
- Dockerized FastAPI app
- Connected to GitHub → auto-deploy on push
- Logs visible in Render dashboard
- Environment variables via Render dashboard

✅ No external CI/CD required → Render handles deploys via GitHub.

✅ No rate limiting or API gateway at this stage.

✅ Monitoring via Render built-in health/status → no third-party monitoring added.

✅ OpenAPI docs accessible via `/v1/docs` post-deploy.

✅ `.env` managed via Render secrets dashboard.

---

## 8️⃣ Folder Structure

```
/constants/
    zodiac_signs.py
    nakshatra_lords.py
    dasha_years.py
    divisional_mappings/d1.py ... d60.py

/services/
    ascendant_service.py
    natal_chart_service.py
    divisional_chart_service.py
    mahadasha_service.py
```

✅ All divisional mapping constants stored in `/constants/divisional_mappings/`.

✅ Constants imported at app startup → cached for performance.

---

## ✅ Conclusion

This document now fully specifies:

- ✅ Celestial bodies
- ✅ Divisional charts D1–D60 with mappings
- ✅ Retrograde handling
- ✅ /v1/ prefix
- ✅ FastAPI docs enabled
- ✅ No rate limiting
- ✅ Render deployment settings
- ✅ Error handling schema
- ✅ Input validation
- ✅ Logging via Render logs

🎉 Complete API functional, technical, deployment specification.

