"""Zodiac sign constants for Vedic astrology"""

from enum import Enum
from typing import Dict, List

class Sign(Enum):
    """Zodiac signs"""
    ARIES = 1
    TAURUS = 2
    GEMINI = 3
    CANCER = 4
    LEO = 5
    VIRGO = 6
    LIBRA = 7
    SCORPIO = 8
    SAGITTARIUS = 9
    CAPRICORN = 10
    AQUARIUS = 11
    PISCES = 12

# Sanskrit names for signs
SIGN_NAMES = {
    Sign.ARIES: "Mesha",
    Sign.TAURUS: "Vrishabha",
    Sign.GEMINI: "Mithuna",
    Sign.CANCER: "Karka",
    Sign.LEO: "Simha",
    Sign.VIRGO: "Kanya",
    Sign.LIBRA: "Tula",
    Sign.SCORPIO: "Vrishchika",
    Sign.SAGITTARIUS: "Dhanu",
    Sign.CAPRICORN: "Makara",
    Sign.AQUARIUS: "Kumbha",
    Sign.PISCES: "Meena"
}

# Sign elements
SIGN_ELEMENTS = {
    Sign.ARIES: "Fire",
    Sign.TAURUS: "Earth",
    Sign.GEMINI: "Air",
    Sign.CANCER: "Water",
    Sign.LEO: "Fire",
    Sign.VIRGO: "Earth",
    Sign.LIBRA: "Air",
    Sign.SCORPIO: "Water",
    Sign.SAGITTARIUS: "Fire",
    Sign.CAPRICORN: "Earth",
    Sign.AQUARIUS: "Air",
    Sign.PISCES: "Water"
}

# Sign qualities
SIGN_QUALITIES = {
    Sign.ARIES: "Cardinal",
    Sign.TAURUS: "Fixed",
    Sign.GEMINI: "Mutable",
    Sign.CANCER: "Cardinal",
    Sign.LEO: "Fixed",
    Sign.VIRGO: "Mutable",
    Sign.LIBRA: "Cardinal",
    Sign.SCORPIO: "Fixed",
    Sign.SAGITTARIUS: "Mutable",
    Sign.CAPRICORN: "Cardinal",
    Sign.AQUARIUS: "Fixed",
    Sign.PISCES: "Mutable"
}

# Sign degrees
SIGN_DEGREES = 30  # Each sign is 30 degrees

# Sign spans in decimal degrees
SIGN_SPAN = 30.0  # 30 degrees in decimal 