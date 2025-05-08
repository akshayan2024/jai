"""
Test server for JAI API
Provides mock responses for all endpoints tested in the test suite
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Create FastAPI app
app = FastAPI(
    title="JAI Test API",
    description="Test API for validating the test suite",
    version="1.0.0",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "Welcome to JAI API - Jyotish Astrological Interpretation",
        "documentation": "/v1/docs",
        "status": "online"
    }

# Health check
@app.get("/v1/api/health")
async def health_check():
    return {
        "status": "healthy",
        "version": "1.0.0",
        "environment": "testing"
    }

# Basic horoscope endpoints - both path patterns
@app.post("/v1/api/horoscope")
@app.post("/api/v1/horoscope")
async def get_horoscope(request: Request):
    """Generate a basic horoscope response"""
    data = await request.json()
    
    # Check if it's the Chennai birth case
    is_chennai_case = (
        data.get("birth_date") == "1988-12-01" or 
        data.get("dateOfBirth") == "1988-12-01"
    )
    
    if is_chennai_case:
        # Return Chennai-specific data
        return {
            "birth_data": {
                "date": data.get("birth_date") or data.get("dateOfBirth"),
                "time": data.get("birth_time") or (data.get("timeOfBirth") + ":00" if data.get("timeOfBirth") else None),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "timezone_offset": data.get("timezone_offset") or data.get("timezone"),
                "ayanamsa": data.get("ayanamsa")
            },
            "ascendant": {
                "ascendant_degree": 15.23,
                "sign_index": 6,
                "ascendant_sign_name": "Virgo"
            },
            "planets": [
                {"planet": "Sun", "longitude": 15.45, "sign_index": 8, "sign_name": "Scorpio", "house": 5, "is_retrograde": False},
                {"planet": "Moon", "longitude": 28.67, "sign_index": 3, "sign_name": "Cancer", "house": 4, "is_retrograde": False},
                {"planet": "Mars", "longitude": 12.89, "sign_index": 7, "sign_name": "Libra", "house": 2, "is_retrograde": False},
                {"planet": "Mercury", "longitude": 23.12, "sign_index": 8, "sign_name": "Scorpio", "house": 5, "is_retrograde": True},
                {"planet": "Jupiter", "longitude": 18.34, "sign_index": 1, "sign_name": "Taurus", "house": 8, "is_retrograde": False},
                {"planet": "Venus", "longitude": 5.56, "sign_index": 9, "sign_name": "Sagittarius", "house": 6, "is_retrograde": False},
                {"planet": "Saturn", "longitude": 28.78, "sign_index": 2, "sign_name": "Gemini", "house": 10, "is_retrograde": True},
                {"planet": "Rahu", "longitude": 15.90, "sign_index": 0, "sign_name": "Aquarius", "house": 2, "is_retrograde": False},
                {"planet": "Ketu", "longitude": 15.90, "sign_index": 6, "sign_name": "Virgo", "house": 8, "is_retrograde": False}
            ],
            "mahadasha": [
                {
                    "planet": "Jupiter",
                    "start_date": "1988-12-01",
                    "end_date": "2004-12-01",
                    "years": 16
                },
                {
                    "planet": "Saturn",
                    "start_date": "2004-12-01",
                    "end_date": "2023-12-01",
                    "years": 19
                }
            ],
            "generated_at": datetime.now().isoformat()
        }
    else:
        # Return generic data
        return {
            "birth_data": {
                "date": data.get("birth_date") or data.get("dateOfBirth"),
                "time": data.get("birth_time") or (data.get("timeOfBirth") + ":00" if data.get("timeOfBirth") else None),
                "latitude": data.get("latitude"),
                "longitude": data.get("longitude"),
                "timezone_offset": data.get("timezone_offset") or data.get("timezone"),
                "ayanamsa": data.get("ayanamsa")
            },
            "ascendant": {
                "ascendant_degree": 45.67,
                "sign_index": 2,
                "ascendant_sign_name": "Taurus"
            },
            "planets": [
                {"planet": "Sun", "longitude": 15.23, "sign_index": 5, "sign_name": "Leo", "house": 5, "is_retrograde": False},
                {"planet": "Moon", "longitude": 12.34, "sign_index": 11, "sign_name": "Pisces", "house": 4, "is_retrograde": False},
                {"planet": "Mars", "longitude": 28.45, "sign_index": 8, "sign_name": "Scorpio", "house": 2, "is_retrograde": False},
                {"planet": "Mercury", "longitude": 28.56, "sign_index": 5, "sign_name": "Leo", "house": 5, "is_retrograde": True},
                {"planet": "Jupiter", "longitude": 15.67, "sign_index": 2, "sign_name": "Taurus", "house": 8, "is_retrograde": False},
                {"planet": "Venus", "longitude": 23.78, "sign_index": 6, "sign_name": "Virgo", "house": 6, "is_retrograde": False},
                {"planet": "Saturn", "longitude": 18.89, "sign_index": 9, "sign_name": "Sagittarius", "house": 10, "is_retrograde": True},
                {"planet": "Rahu", "longitude": 12.90, "sign_index": 3, "sign_name": "Gemini", "house": 2, "is_retrograde": False},
                {"planet": "Ketu", "longitude": 12.90, "sign_index": 9, "sign_name": "Sagittarius", "house": 8, "is_retrograde": False}
            ],
            "mahadasha": [
                {
                    "planet": "Saturn",
                    "start_date": (datetime.now() - timedelta(days=365*5)).strftime("%Y-%m-%d"),
                    "end_date": (datetime.now() + timedelta(days=365*14)).strftime("%Y-%m-%d"),
                    "years": 19
                },
                {
                    "planet": "Mercury",
                    "start_date": (datetime.now() + timedelta(days=365*14)).strftime("%Y-%m-%d"),
                    "end_date": (datetime.now() + timedelta(days=365*(14+17))).strftime("%Y-%m-%d"),
                    "years": 17
                }
            ],
            "generated_at": datetime.now().isoformat()
        }

# Divisional charts endpoint
@app.post("/v1/api/horoscope/divisional")
async def get_divisional_charts(request: Request):
    """Generate divisional charts"""
    data = await request.json()
    
    return {
        "navamsa": {
            "ascendant": {
                "sign_index": 2,
                "degree": 18.45
            },
            "planets": [
                {"planet": "Sun", "sign_index": 3, "degree": 15.45},
                {"planet": "Moon", "sign_index": 5, "degree": 28.67},
                {"planet": "Mars", "sign_index": 7, "degree": 12.89},
                {"planet": "Mercury", "sign_index": 3, "degree": 23.12},
                {"planet": "Jupiter", "sign_index": 9, "degree": 18.34},
                {"planet": "Venus", "sign_index": 11, "degree": 5.56},
                {"planet": "Saturn", "sign_index": 1, "degree": 28.78},
                {"planet": "Rahu", "sign_index": 2, "degree": 15.90},
                {"planet": "Ketu", "sign_index": 8, "degree": 15.90}
            ]
        },
        "dasamsa": {
            "ascendant": {
                "sign_index": 9,
                "degree": 12.67
            },
            "planets": [
                {"planet": "Sun", "sign_index": 3, "degree": 15.45},
                {"planet": "Moon", "sign_index": 5, "degree": 28.67},
                {"planet": "Mars", "sign_index": 7, "degree": 12.89},
                {"planet": "Mercury", "sign_index": 3, "degree": 23.12},
                {"planet": "Jupiter", "sign_index": 9, "degree": 18.34},
                {"planet": "Venus", "sign_index": 11, "degree": 5.56},
                {"planet": "Saturn", "sign_index": 1, "degree": 28.78},
                {"planet": "Rahu", "sign_index": 2, "degree": 15.90},
                {"planet": "Ketu", "sign_index": 8, "degree": 15.90}
            ]
        },
        "chaturvimshamsa": {
            "ascendant": {
                "sign_index": 5,
                "degree": 23.89
            },
            "planets": [
                {"planet": "Sun", "sign_index": 3, "degree": 15.45},
                {"planet": "Moon", "sign_index": 5, "degree": 28.67},
                {"planet": "Mars", "sign_index": 7, "degree": 12.89},
                {"planet": "Mercury", "sign_index": 3, "degree": 23.12},
                {"planet": "Jupiter", "sign_index": 9, "degree": 18.34},
                {"planet": "Venus", "sign_index": 11, "degree": 5.56},
                {"planet": "Saturn", "sign_index": 1, "degree": 28.78},
                {"planet": "Rahu", "sign_index": 2, "degree": 15.90},
                {"planet": "Ketu", "sign_index": 8, "degree": 15.90}
            ]
        }
    }

# All divisional charts endpoint
@app.post("/v1/api/horoscope/divisional/all")
async def get_all_divisional_charts(request: Request):
    """Generate all divisional charts"""
    data = await request.json()
    
    divisional_response = {}
    divisions = ["d-1", "d-2", "d-3", "d-4", "d-7", "d-9", "d-10", "d-12", "d-16", "d-20", "d-24", "d-27", "d-30", "d-40", "d-45", "d-60"]
    
    for div in divisions:
        divisional_response[div] = {
            "ascendant": {
                "sign_index": 6 if div not in ["d-9", "d-10", "d-24"] else (2 if div == "d-9" else (9 if div == "d-10" else 5)),
                "degree": 15.23 if div not in ["d-9", "d-10", "d-24"] else (18.45 if div == "d-9" else (12.67 if div == "d-10" else 23.89))
            },
            "planets": [
                {"planet": "Sun", "sign_index": 8, "degree": 15.45},
                {"planet": "Moon", "sign_index": 3, "degree": 28.67},
                {"planet": "Mars", "sign_index": 7, "degree": 12.89},
                {"planet": "Mercury", "sign_index": 8, "degree": 23.12},
                {"planet": "Jupiter", "sign_index": 1, "degree": 18.34},
                {"planet": "Venus", "sign_index": 9, "degree": 5.56},
                {"planet": "Saturn", "sign_index": 2, "degree": 28.78},
                {"planet": "Rahu", "sign_index": 0, "degree": 15.90},
                {"planet": "Ketu", "sign_index": 6, "degree": 15.90}
            ]
        }
    
    return divisional_response

# Yogas endpoint
@app.post("/v1/api/horoscope/yogas")
async def get_yogas(request: Request):
    """Generate yoga formations"""
    data = await request.json()
    
    return {
        "yogas": [
            {
                "name": "Budha-Aditya Yoga",
                "planets": ["Mercury", "Sun"],
                "house": 8,
                "type": "conjunction"
            },
            {
                "name": "Gaja-Kesari Yoga",
                "planets": ["Jupiter", "Moon"],
                "type": "trine"
            }
        ]
    }

# All yogas endpoint
@app.post("/v1/api/horoscope/yogas/all")
async def get_all_yogas(request: Request):
    """Generate all yoga formations"""
    data = await request.json()
    
    return {
        "yogas": [
            {
                "name": "Budha-Aditya Yoga",
                "planets": ["Mercury", "Sun"],
                "house": 8,
                "type": "conjunction"
            },
            {
                "name": "Gaja-Kesari Yoga",
                "planets": ["Jupiter", "Moon"],
                "type": "trine"
            },
            {
                "name": "Kemadruma Yoga",
                "planets": ["Moon"],
                "type": "special"
            },
            {
                "name": "Raja Yoga",
                "planets": ["Jupiter", "Venus"],
                "type": "conjunction"
            },
            {
                "name": "Dharma-Karmadhipati Yoga",
                "planets": ["Jupiter", "Saturn"],
                "type": "conjunction"
            }
        ]
    }

# House positions endpoint
@app.post("/v1/api/horoscope/houses")
async def get_house_positions(request: Request):
    """Generate house positions"""
    data = await request.json()
    
    return {
        "houses": [
            {"sign_index": 6, "degree": 15.23},  # 1st House
            {"sign_index": 7, "degree": 15.23},  # 2nd House
            {"sign_index": 8, "degree": 15.23},  # 3rd House
            {"sign_index": 9, "degree": 15.23},  # 4th House
            {"sign_index": 10, "degree": 15.23},  # 5th House
            {"sign_index": 11, "degree": 15.23},  # 6th House
            {"sign_index": 0, "degree": 15.23},  # 7th House
            {"sign_index": 1, "degree": 15.23},  # 8th House
            {"sign_index": 2, "degree": 15.23},  # 9th House
            {"sign_index": 3, "degree": 15.23},  # 10th House
            {"sign_index": 4, "degree": 15.23},  # 11th House
            {"sign_index": 5, "degree": 15.23}   # 12th House
        ],
        "aspects": [
            {"from_planet": "Jupiter", "to_planet": "Moon", "type": "trine", "orb": 2.5},
            {"from_planet": "Jupiter", "to_planet": "Saturn", "type": "opposition", "orb": 1.2},
            {"from_planet": "Jupiter", "to_planet": "Mars", "type": "square", "orb": 3.1}
        ]
    }

# All house positions endpoint
@app.post("/v1/api/horoscope/houses/all")
async def get_all_house_positions(request: Request):
    """Generate all house positions"""
    data = await request.json()
    
    return {
        "houses": [
            {"sign_index": 6, "degree": 15.23},  # 1st House
            {"sign_index": 7, "degree": 15.23},  # 2nd House
            {"sign_index": 8, "degree": 15.23},  # 3rd House
            {"sign_index": 9, "degree": 15.23},  # 4th House
            {"sign_index": 10, "degree": 15.23},  # 5th House
            {"sign_index": 11, "degree": 15.23},  # 6th House
            {"sign_index": 0, "degree": 15.23},  # 7th House
            {"sign_index": 1, "degree": 15.23},  # 8th House
            {"sign_index": 2, "degree": 15.23},  # 9th House
            {"sign_index": 3, "degree": 15.23},  # 10th House
            {"sign_index": 4, "degree": 15.23},  # 11th House
            {"sign_index": 5, "degree": 15.23}   # 12th House
        ],
        "aspects": [
            {"from_planet": "Jupiter", "to_planet": "Moon", "type": "trine", "orb": 2.5},
            {"from_planet": "Jupiter", "to_planet": "Saturn", "type": "opposition", "orb": 1.2},
            {"from_planet": "Jupiter", "to_planet": "Mars", "type": "square", "orb": 3.1},
            {"from_planet": "Sun", "to_planet": "Mercury", "type": "conjunction", "orb": 0.5},
            {"from_planet": "Venus", "to_planet": "Jupiter", "type": "sextile", "orb": 2.3}
        ],
        "special_aspects": {
            "mutual_aspects": [
                {"planets": ["Jupiter", "Saturn"], "type": "opposition"}
            ],
            "planetary_war": [
                {"planets": ["Sun", "Mercury"], "winner": "Sun"}
            ],
            "combust": [
                {"planet": "Mercury", "combustor": "Sun", "orb": 3.5}
            ]
        }
    }

# Dasha endpoint
@app.post("/v1/api/horoscope/dasha")
async def get_dasha(request: Request):
    """Generate dasha periods"""
    data = await request.json()
    
    return {
        "mahadasha": [
            {
                "planet": "Jupiter",
                "start_date": "1988-12-01",
                "end_date": "2004-12-01",
                "years": 16
            },
            {
                "planet": "Saturn",
                "start_date": "2004-12-01",
                "end_date": "2023-12-01",
                "years": 19
            },
            {
                "planet": "Mercury",
                "start_date": "2023-12-01",
                "end_date": "2040-12-01",
                "years": 17
            },
            {
                "planet": "Ketu",
                "start_date": "2040-12-01",
                "end_date": "2047-12-01",
                "years": 7
            },
            {
                "planet": "Venus",
                "start_date": "2047-12-01",
                "end_date": "2067-12-01",
                "years": 20
            },
            {
                "planet": "Sun",
                "start_date": "2067-12-01",
                "end_date": "2073-12-01",
                "years": 6
            },
            {
                "planet": "Moon",
                "start_date": "2073-12-01",
                "end_date": "2083-12-01",
                "years": 10
            },
            {
                "planet": "Mars",
                "start_date": "2083-12-01",
                "end_date": "2090-12-01",
                "years": 7
            },
            {
                "planet": "Rahu",
                "start_date": "2090-12-01",
                "end_date": "2108-12-01",
                "years": 18
            }
        ],
        "antardasha": [
            {
                "mahadasha": "Jupiter",
                "periods": [
                    {
                        "planet": "Jupiter",
                        "start_date": "1988-12-01",
                        "end_date": "1990-12-01",
                        "years": 2
                    },
                    {
                        "planet": "Saturn",
                        "start_date": "1990-12-01",
                        "end_date": "1993-09-30",
                        "years": 2.83
                    }
                ]
            }
        ]
    }

# All dasha periods endpoint
@app.post("/v1/api/horoscope/dasha/all")
async def get_all_dasha_periods(request: Request):
    """Generate all dasha periods"""
    data = await request.json()
    
    return {
        "mahadasha": [
            {
                "planet": "Jupiter",
                "start_date": "1988-12-01",
                "end_date": "2004-12-01",
                "years": 16
            },
            {
                "planet": "Saturn",
                "start_date": "2004-12-01",
                "end_date": "2023-12-01",
                "years": 19
            },
            {
                "planet": "Mercury",
                "start_date": "2023-12-01",
                "end_date": "2040-12-01",
                "years": 17
            },
            {
                "planet": "Ketu",
                "start_date": "2040-12-01",
                "end_date": "2047-12-01",
                "years": 7
            },
            {
                "planet": "Venus",
                "start_date": "2047-12-01",
                "end_date": "2067-12-01",
                "years": 20
            },
            {
                "planet": "Sun",
                "start_date": "2067-12-01",
                "end_date": "2073-12-01",
                "years": 6
            },
            {
                "planet": "Moon",
                "start_date": "2073-12-01",
                "end_date": "2083-12-01",
                "years": 10
            },
            {
                "planet": "Mars",
                "start_date": "2083-12-01",
                "end_date": "2090-12-01",
                "years": 7
            },
            {
                "planet": "Rahu",
                "start_date": "2090-12-01",
                "end_date": "2108-12-01",
                "years": 18
            }
        ],
        "antardasha": [
            {
                "mahadasha": "Jupiter",
                "periods": [
                    {
                        "planet": "Jupiter",
                        "start_date": "1988-12-01",
                        "end_date": "1990-12-01",
                        "years": 2
                    },
                    {
                        "planet": "Saturn",
                        "start_date": "1990-12-01",
                        "end_date": "1993-09-30",
                        "years": 2.83
                    },
                    {
                        "planet": "Mercury",
                        "start_date": "1993-09-30",
                        "end_date": "1996-04-15",
                        "years": 2.5
                    },
                    {
                        "planet": "Ketu",
                        "start_date": "1996-04-15",
                        "end_date": "1997-04-15",
                        "years": 1
                    },
                    {
                        "planet": "Venus",
                        "start_date": "1997-04-15",
                        "end_date": "2000-04-15",
                        "years": 3
                    },
                    {
                        "planet": "Sun",
                        "start_date": "2000-04-15",
                        "end_date": "2001-01-15",
                        "years": 0.75
                    },
                    {
                        "planet": "Moon",
                        "start_date": "2001-01-15",
                        "end_date": "2002-05-15",
                        "years": 1.33
                    },
                    {
                        "planet": "Mars",
                        "start_date": "2002-05-15",
                        "end_date": "2003-04-15",
                        "years": 0.92
                    },
                    {
                        "planet": "Rahu",
                        "start_date": "2003-04-15",
                        "end_date": "2004-12-01",
                        "years": 1.67
                    }
                ]
            },
            {
                "mahadasha": "Saturn",
                "periods": [
                    {
                        "planet": "Saturn",
                        "start_date": "2004-12-01",
                        "end_date": "2007-12-01",
                        "years": 3
                    },
                    {
                        "planet": "Mercury",
                        "start_date": "2007-12-01",
                        "end_date": "2010-09-15",
                        "years": 2.8
                    }
                ]
            },
            {
                "mahadasha": "Mercury",
                "periods": [
                    {
                        "planet": "Mercury",
                        "start_date": "2023-12-01",
                        "end_date": "2026-10-15",
                        "years": 2.9
                    },
                    {
                        "planet": "Ketu",
                        "start_date": "2026-10-15",
                        "end_date": "2028-01-01",
                        "years": 1.2
                    }
                ]
            }
        ],
        "pratyantardasha": [
            {
                "mahadasha": "Jupiter",
                "periods": [
                    {
                        "antardasha": "Jupiter",
                        "planet": "Jupiter",
                        "start_date": "1988-12-01",
                        "end_date": "1989-03-15",
                        "months": 3.5
                    }
                ]
            },
            {
                "mahadasha": "Saturn",
                "periods": [
                    {
                        "antardasha": "Saturn",
                        "planet": "Saturn",
                        "start_date": "2004-12-01",
                        "end_date": "2005-06-15",
                        "months": 6.5
                    }
                ]
            }
        ]
    }

# Transits endpoint
@app.post("/v1/api/horoscope/transits")
@app.post("/v1/api/horoscope/transits/all")
async def get_transits(request: Request):
    """Generate transit positions"""
    data = await request.json()
    
    return {
        "transits": [
            {"planet": "Sun", "sign_index": 2, "degree": 15.45, "house": 9, "retrograde": False},
            {"planet": "Moon", "sign_index": 7, "degree": 28.67, "house": 2, "retrograde": False},
            {"planet": "Mars", "sign_index": 5, "degree": 12.89, "house": 12, "retrograde": False},
            {"planet": "Mercury", "sign_index": 1, "degree": 23.12, "house": 8, "retrograde": True},
            {"planet": "Jupiter", "sign_index": 8, "degree": 18.34, "house": 3, "retrograde": False},
            {"planet": "Venus", "sign_index": 3, "degree": 5.56, "house": 10, "retrograde": False},
            {"planet": "Saturn", "sign_index": 11, "degree": 28.78, "house": 6, "retrograde": True},
            {"planet": "Rahu", "sign_index": 4, "degree": 15.90, "house": 11, "retrograde": False},
            {"planet": "Ketu", "sign_index": 10, "degree": 15.90, "house": 5, "retrograde": False}
        ],
        "aspects": [
            {"from_planet": "Jupiter", "to_planet": "Moon", "type": "trine", "orb": 2.5},
            {"from_planet": "Jupiter", "to_planet": "Saturn", "type": "opposition", "orb": 1.2},
            {"from_planet": "Jupiter", "to_planet": "Mars", "type": "square", "orb": 3.1},
            {"from_planet": "Sun", "to_planet": "Mercury", "type": "sextile", "orb": 0.5},
            {"from_planet": "Venus", "to_planet": "Jupiter", "type": "square", "orb": 2.3}
        ],
        "natal_aspects": [
            {"transit_planet": "Jupiter", "natal_planet": "Moon", "type": "conjunction", "orb": 1.2},
            {"transit_planet": "Saturn", "natal_planet": "Sun", "type": "opposition", "orb": 2.3}
        ],
        "special_transits": {
            "retrograde": ["Mercury", "Saturn"],
            "combust": ["Mercury"],
            "exaltation": ["Venus"],
            "debilitation": ["Saturn"]
        }
    }

# Run the server
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 