"""
DEPRECATED: This module is deprecated and will be removed in a future version.
Please use `api.constants.nakshatras` instead.

This module provided nakshatra (lunar mansion) constants and utilities for Vedic astrology.
All functionality has been moved to `api.constants.nakshatras` for better organization.

To migrate, update your imports:

Old: from constants.nakshatras import NAKSHATRA_NAMES, get_nakshatra_name
New: from api.constants.nakshatras import NAKSHATRA_NAMES, get_nakshatra_name
"""

import warnings
from typing import Any, Dict, List, Tuple, Optional

# Import everything from the new location
from api.constants.nakshatras import (
    NAKSHATRA_NAMES,
    NAKSHATRA_LORDS,
    NAKSHATRA_SPAN,
    NAKSHATRA_COUNT,
    PADA_COUNT,
    PADA_SPAN,
    get_nakshatra_index,
    get_nakshatra_name,
    get_nakshatra_lord,
    get_nakshatra_pada,
    get_degrees_in_nakshatra
)

# Issue deprecation warning
warnings.warn(
    "The constants.nakshatras module is deprecated. "
    "Please use api.constants.nakshatras instead.",
    DeprecationWarning,
    stacklevel=2
)

# Re-export all symbols from the new module to maintain backward compatibility
__all__ = [
    'NAKSHATRA_NAMES',
    'NAKSHATRA_LORDS',
    'NAKSHATRA_SPAN',
    'NAKSHATRA_COUNT',
    'PADA_COUNT',
    'PADA_SPAN',
    'get_nakshatra_index',
    'get_nakshatra_name',
    'get_nakshatra_lord',
    'get_nakshatra_pada',
    'get_degrees_in_nakshatra'
]