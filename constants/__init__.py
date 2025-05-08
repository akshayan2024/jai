"""
Constants package exports and cache management.
"""

# Global cache for constants
_CONSTANTS_CACHE = {}

def load_all_constants():
    """Load all constants into memory cache."""
    # Load zodiac signs
    from .zodiac_signs import ZODIAC_SIGNS
    _CONSTANTS_CACHE['zodiac_signs'] = ZODIAC_SIGNS
    
    # Load planets
    from .planets import PLANETS, PLANET_NAMES, SWE_CODE_TO_PLANET
    _CONSTANTS_CACHE['planets'] = PLANETS
    _CONSTANTS_CACHE['planet_names'] = PLANET_NAMES
    _CONSTANTS_CACHE['swe_code_to_planet'] = SWE_CODE_TO_PLANET
    
    # Load nakshatras
    from .nakshatras import NAKSHATRAS, get_nakshatra_from_longitude
    _CONSTANTS_CACHE['nakshatras'] = NAKSHATRAS
    _CONSTANTS_CACHE['get_nakshatra_from_longitude'] = get_nakshatra_from_longitude
    
    # Load dasha years
    from .dasha_years import DASHA_YEARS, TOTAL_DASHA_YEARS, NAKSHATRA_LORDS
    _CONSTANTS_CACHE['dasha_years'] = DASHA_YEARS
    _CONSTANTS_CACHE['total_dasha_years'] = TOTAL_DASHA_YEARS
    _CONSTANTS_CACHE['nakshatra_lords'] = NAKSHATRA_LORDS
    
    # Load ayanamsa constants
    from .ayanamsa import (
        AYANAMSA_LAHIRI, AYANAMSA_RAMAN, AYANAMSA_KRISHNAMURTI,
        DEFAULT_AYANAMSA, AYANAMSA_MAPPING, AYANAMSA_NAMES
    )
    _CONSTANTS_CACHE['ayanamsa_lahiri'] = AYANAMSA_LAHIRI
    _CONSTANTS_CACHE['ayanamsa_raman'] = AYANAMSA_RAMAN
    _CONSTANTS_CACHE['ayanamsa_krishnamurti'] = AYANAMSA_KRISHNAMURTI
    _CONSTANTS_CACHE['default_ayanamsa'] = DEFAULT_AYANAMSA
    _CONSTANTS_CACHE['ayanamsa_mapping'] = AYANAMSA_MAPPING
    _CONSTANTS_CACHE['ayanamsa_names'] = AYANAMSA_NAMES
    
    # Load divisional mappings
    from .divisional_mappings import DIVISIONAL_MAPPINGS
    _CONSTANTS_CACHE['divisional_mappings'] = DIVISIONAL_MAPPINGS
    
    # Validate all loaded constants
    _validate_constants()
    
    return _CONSTANTS_CACHE

def _validate_constants():
    """
    Validate that all constants are properly defined.
    This helps catch any issues at startup rather than during runtime.
    """
    # Make sure zodiac signs are numbered 1-12
    zodiac_signs = _CONSTANTS_CACHE.get('zodiac_signs', {})
    if not all(1 <= idx <= 12 for idx in zodiac_signs.keys()):
        raise ValueError("Zodiac signs must be indexed from 1 to 12")
    
    # Make sure planets are numbered 1-9
    planets = _CONSTANTS_CACHE.get('planets', {})
    if not all(1 <= idx <= 9 for idx in planets.keys()):
        raise ValueError("Planets must be indexed from 1 to 9")
    
    # Make sure nakshatras are numbered 1-27
    nakshatras = _CONSTANTS_CACHE.get('nakshatras', {})
    if not all(1 <= idx <= 27 for idx in nakshatras.keys()):
        raise ValueError("Nakshatras must be indexed from 1 to 27")
    
    # Make sure divisional mappings are consistent
    divisional_mappings = _CONSTANTS_CACHE.get('divisional_mappings', {})
    for chart_name, mapping in divisional_mappings.items():
        # Check that all signs are mapped
        if not all(1 <= sign <= 12 for sign in mapping.keys()):
            raise ValueError(f"All signs must be mapped in {chart_name}")
            
        # For each divisional mapping, check that values are valid signs
        for sign, divisions in mapping.items():
            if not all(1 <= mapped_sign <= 12 for mapped_sign in divisions.values()):
                raise ValueError(f"Invalid sign mapping in {chart_name} for sign {sign}")

def get_constant(category, key=None):
    """
    Get constant from cache.
    
    Args:
        category: Constant category name
        key: Optional specific key for dictionaries
        
    Returns:
        Requested constant or None if not found
    """
    if not _CONSTANTS_CACHE:
        load_all_constants()
    
    if key is None:
        return _CONSTANTS_CACHE.get(category)
    
    return _CONSTANTS_CACHE.get(category, {}).get(key)

# Export the cache management functions
__all__ = ['load_all_constants', 'get_constant'] 