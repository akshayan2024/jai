"""
Componentized Test server for JAI API
Provides separate endpoints for each astrological component
"""

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from datetime import datetime, timedelta
from typing import Dict, Any, List, Optional

# Create FastAPI app
app = FastAPI(
    title="JAI Componentized API",
    description="Test API for validating the test suite with componentized endpoints",
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
        "message": "Welcome to JAI API - Jyotish Astrological Interpretation (Componentized)",
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

# Ascendant component
@app.post("/v1/api/horoscope/ascendant")
async def get_ascendant(request: Request):
    """Get only the ascendant component"""
    data = await request.json()
    
    # Check if it's the Chennai birth case
    is_chennai_case = (
        data.get("birth_date") == "1988-12-01" or 
        data.get("dateOfBirth") == "1988-12-01"
    )
    
    if is_chennai_case:
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
            }
        }
    else:
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
            }
        }

# Planets component (D-1 chart)
@app.post("/v1/api/horoscope/planets")
@app.post("/v1/api/horoscope/d1")
async def get_planets(request: Request):
    """Get only the planets component (D-1 chart)"""
    data = await request.json()
    
    # Check if it's the Chennai birth case
    is_chennai_case = (
        data.get("birth_date") == "1988-12-01" or 
        data.get("dateOfBirth") == "1988-12-01"
    )
    
    if is_chennai_case:
        return {
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
            ]
        }
    else:
        return {
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
            ]
        }

# Individual divisional chart endpoints
@app.post("/v1/api/horoscope/d{division}")
async def get_divisional_chart(division: int, request: Request):
    """Get a specific divisional chart"""
    data = await request.json()
    
    valid_divisions = [1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, 60]
    if division not in valid_divisions:
        return {"error": f"Invalid division D-{division}. Valid divisions are: {', '.join([f'D-{d}' for d in valid_divisions])}"}
    
    # Special cases for D-9, D-10, and D-24
    if division == 9:
        return {
            "d9": {
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
            }
        }
    elif division == 10:
        return {
            "d10": {
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
            }
        }
    elif division == 24:
        return {
            "d24": {
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
    else:
        # Generic response for other divisions
        return {
            f"d{division}": {
                "ascendant": {
                    "sign_index": 6,
                    "degree": 15.23
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
        }

# Mahadasha component
@app.post("/v1/api/horoscope/mahadasha")
async def get_mahadasha(request: Request):
    """Get only the mahadasha component"""
    data = await request.json()
    
    # Check if it's the Chennai birth case
    is_chennai_case = (
        data.get("birth_date") == "1988-12-01" or 
        data.get("dateOfBirth") == "1988-12-01"
    )
    
    if is_chennai_case:
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
            ]
        }
    else:
        return {
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
            ]
        }

# Antardasha component
@app.post("/v1/api/horoscope/antardasha")
async def get_antardasha(request: Request):
    """Get only the antardasha component"""
    data = await request.json()
    
    # Check if it's the Chennai birth case
    is_chennai_case = (
        data.get("birth_date") == "1988-12-01" or 
        data.get("dateOfBirth") == "1988-12-01"
    )
    
    if is_chennai_case:
        return {
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
                }
            ]
        }
    else:
        return {
            "antardasha": [
                {
                    "mahadasha": "Saturn",
                    "periods": [
                        {
                            "planet": "Saturn",
                            "start_date": (datetime.now() - timedelta(days=365*2)).strftime("%Y-%m-%d"),
                            "end_date": (datetime.now() + timedelta(days=365*1)).strftime("%Y-%m-%d"),
                            "years": 3
                        },
                        {
                            "planet": "Mercury",
                            "start_date": (datetime.now() + timedelta(days=365*1)).strftime("%Y-%m-%d"),
                            "end_date": (datetime.now() + timedelta(days=365*3.8)).strftime("%Y-%m-%d"),
                            "years": 2.8
                        }
                    ]
                }
            ]
        }

# Pratyantardasha component
@app.post("/v1/api/horoscope/pratyantardasha")
async def get_pratyantardasha(request: Request):
    """Get only the pratyantardasha component"""
    data = await request.json()
    
    # Check if it's the Chennai birth case
    is_chennai_case = (
        data.get("birth_date") == "1988-12-01" or 
        data.get("dateOfBirth") == "1988-12-01"
    )
    
    if is_chennai_case:
        return {
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
                        },
                        {
                            "antardasha": "Jupiter",
                            "planet": "Saturn",
                            "start_date": "1989-03-15",
                            "end_date": "1989-06-30",
                            "months": 3.5
                        },
                        {
                            "antardasha": "Jupiter",
                            "planet": "Mercury",
                            "start_date": "1989-06-30",
                            "end_date": "1989-10-15",
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
                        },
                        {
                            "antardasha": "Saturn",
                            "planet": "Mercury",
                            "start_date": "2005-06-15",
                            "end_date": "2005-12-31",
                            "months": 6.5
                        }
                    ]
                }
            ]
        }
    else:
        return {
            "pratyantardasha": [
                {
                    "mahadasha": "Saturn",
                    "periods": [
                        {
                            "antardasha": "Saturn",
                            "planet": "Saturn",
                            "start_date": (datetime.now() - timedelta(days=90)).strftime("%Y-%m-%d"),
                            "end_date": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"),
                            "months": 6
                        },
                        {
                            "antardasha": "Saturn",
                            "planet": "Mercury",
                            "start_date": (datetime.now() + timedelta(days=90)).strftime("%Y-%m-%d"),
                            "end_date": (datetime.now() + timedelta(days=180)).strftime("%Y-%m-%d"),
                            "months": 3
                        }
                    ]
                }
            ]
        }

# House positions component
@app.post("/v1/api/horoscope/houses/positions")
async def get_house_positions(request: Request):
    """Get only the house positions component"""
    data = await request.json()
    
    return {
        "houses": [
            {"sign_index": 6, "degree": 15.23, "house_number": 1},  # 1st House
            {"sign_index": 7, "degree": 15.23, "house_number": 2},  # 2nd House
            {"sign_index": 8, "degree": 15.23, "house_number": 3},  # 3rd House
            {"sign_index": 9, "degree": 15.23, "house_number": 4},  # 4th House
            {"sign_index": 10, "degree": 15.23, "house_number": 5},  # 5th House
            {"sign_index": 11, "degree": 15.23, "house_number": 6},  # 6th House
            {"sign_index": 0, "degree": 15.23, "house_number": 7},  # 7th House
            {"sign_index": 1, "degree": 15.23, "house_number": 8},  # 8th House
            {"sign_index": 2, "degree": 15.23, "house_number": 9},  # 9th House
            {"sign_index": 3, "degree": 15.23, "house_number": 10},  # 10th House
            {"sign_index": 4, "degree": 15.23, "house_number": 11},  # 11th House
            {"sign_index": 5, "degree": 15.23, "house_number": 12}   # 12th House
        ]
    }

# Aspects component
@app.post("/v1/api/horoscope/aspects")
async def get_aspects(request: Request):
    """Get only the aspects component"""
    data = await request.json()
    
    return {
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

# Yoga formations component
@app.post("/v1/api/horoscope/yogas/individual")
async def get_individual_yogas(request: Request):
    """Get individual yoga formations"""
    data = await request.json()
    
    return {
        "yogas": [
            {
                "name": "Budha-Aditya Yoga",
                "planets": ["Mercury", "Sun"],
                "house": 8,
                "type": "conjunction",
                "description": "Mercury and Sun conjunction yoga which can give intelligence and academic success"
            },
            {
                "name": "Gaja-Kesari Yoga",
                "planets": ["Jupiter", "Moon"],
                "type": "trine",
                "description": "Jupiter and Moon in trine creates this powerful yoga giving success and prosperity"
            },
            {
                "name": "Kemadruma Yoga",
                "planets": ["Moon"],
                "type": "special",
                "description": "Moon without any planets in adjacent houses creates this challenging yoga"
            },
            {
                "name": "Raja Yoga",
                "planets": ["Jupiter", "Venus"],
                "type": "conjunction",
                "description": "Conjunction of lords of auspicious houses creating success and wealth"
            },
            {
                "name": "Dharma-Karmadhipati Yoga",
                "planets": ["Jupiter", "Saturn"],
                "type": "conjunction",
                "description": "Lords of 9th and 10th houses forming a yoga giving career success"
            }
        ]
    }

# Transit positions component
@app.post("/v1/api/horoscope/transits/positions")
async def get_transit_positions(request: Request):
    """Get only the transit positions component"""
    data = await request.json()
    
    return {
        "transit_date": data.get("transit_date", datetime.now().strftime("%Y-%m-%d")),
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
        ]
    }

# Transit aspects component
@app.post("/v1/api/horoscope/transits/aspects")
async def get_transit_aspects(request: Request):
    """Get only the transit aspects component"""
    data = await request.json()
    
    return {
        "transit_date": data.get("transit_date", datetime.now().strftime("%Y-%m-%d")),
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
        ]
    }

# Special transits component
@app.post("/v1/api/horoscope/transits/special")
async def get_special_transits(request: Request):
    """Get only the special transits component"""
    data = await request.json()
    
    return {
        "transit_date": data.get("transit_date", datetime.now().strftime("%Y-%m-%d")),
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