from fastapi import APIRouter, HTTPException, Depends
from datetime import datetime
from typing import List
from api.models.astrological import (
    BirthData, HoroscopeResponse, PlanetPosition,
    HousePosition, Yoga, DashaPeriod
)
from api.services.astrological_calculations import AstrologicalCalculator

router = APIRouter(
    prefix="/v1/api/horoscope",
    tags=["horoscope"]
)

# Create calculator instance
calculator = AstrologicalCalculator()

@router.post("/", response_model=HoroscopeResponse)
async def get_horoscope(birth_data: BirthData):
    """
    Get complete horoscope including ascendant, planets, houses, yogas, and dashas
    """
    try:
        # Calculate ascendant
        ascendant = calculator.calculate_ascendant(birth_data)
        
        # Calculate planet positions
        planets = calculator.calculate_planet_positions(birth_data)
        
        # Calculate houses
        houses = calculator.calculate_houses(birth_data, ascendant)
        
        # Calculate yogas
        yogas = calculator.calculate_yogas(planets, houses)
        
        # Get moon's longitude for dasha calculation
        moon_position = next(p for p in planets if p.planet == Planet.MOON)
        moon_longitude = moon_position.degree + (moon_position.sign.value - 1) * 30
        
        # Calculate dashas
        dashas = calculator.calculate_dashas(birth_data, moon_longitude)
        
        return HoroscopeResponse(
            birth_data=birth_data,
            ascendant=ascendant,
            planets=planets,
            houses=houses,
            yogas=yogas,
            dashas=dashas
        )
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating horoscope: {str(e)}"
        ) 