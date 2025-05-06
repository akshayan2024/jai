"""
Divisional chart mappings package exports.
"""

from .d1 import D1_MAPPING
from .d2 import D2_MAPPING
from .d3 import D3_MAPPING
from .d4 import D4_MAPPING
from .d7 import D7_MAPPING
from .d9 import D9_MAPPING
from .d10 import D10_MAPPING
from .d12 import D12_MAPPING

# Mapping of divisional chart names to their mapping dictionaries
DIVISIONAL_MAPPINGS = {
    "D1": D1_MAPPING,
    "D2": D2_MAPPING,
    "D3": D3_MAPPING,
    "D4": D4_MAPPING,
    "D7": D7_MAPPING,
    "D9": D9_MAPPING,
    "D10": D10_MAPPING,
    "D12": D12_MAPPING,
} 