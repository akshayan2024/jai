"""
API route modules for JAI
"""
from api.routes.ascendant import router as ascendant_router
from api.routes.planets import router as planets_router

# This prevents other route modules from being imported directly
__all__ = [] 