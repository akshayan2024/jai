"""
API route modules for JAI

This module exports all route objects to be included in the main FastAPI application.
Routes should follow a consistent pattern:
1. Define a router with a specific prefix and tags
2. Expose the router with a descriptive name (e.g., planets_router)
"""
from api.routes.ascendant import router as ascendant_router
from api.routes.planets import router as planets_router
from api.routes.horoscope import router as horoscope_router

# Export all routers that should be included in the app
__all__ = ["ascendant_router", "planets_router", "horoscope_router"]

# Add new routers to both the imports above and __all__ list when creating new route modules 