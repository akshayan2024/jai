"""
Ayanamsa definitions for sidereal calculations.
These will map to actual Swiss Ephemeris constants when integrated.
"""

# Ayanamsa constants (these will be mapped to actual Swiss Ephemeris constants)
AYANAMSA_LAHIRI = 1  # Lahiri (Indian)
AYANAMSA_RAMAN = 2   # B.V. Raman (Tamil)
AYANAMSA_KRISHNAMURTI = 3  # K.S. Krishnamurti (KP)

# Default ayanamsa
DEFAULT_AYANAMSA = AYANAMSA_LAHIRI

# Name to code mapping
AYANAMSA_MAPPING = {
    "lahiri": AYANAMSA_LAHIRI,
    "raman": AYANAMSA_RAMAN,
    "krishnamurti": AYANAMSA_KRISHNAMURTI
}

# Code to name mapping
AYANAMSA_NAMES = {
    AYANAMSA_LAHIRI: "lahiri",
    AYANAMSA_RAMAN: "raman",
    AYANAMSA_KRISHNAMURTI: "krishnamurti"
} 