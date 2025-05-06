import logging
from fastapi import FastAPI, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

from .routes import health
from .routes.v1 import ascendant, natal_chart, divisional_chart, mahadasha, nakshatra, aspect, yoga
from .utils.error_handlers import custom_exception_handler
from .utils.logger import setup_logging
from .constants import load_all_constants

# Initialize logging
logger = setup_logging()

# Create FastAPI application
app = FastAPI(
    title="JAI Astrological API",
    description="""
    API for Vedic astrological calculations based on the Swiss Ephemeris.
    
    ## Features
    
    * Ascendant calculation
    * Natal chart (D1) with planet positions
    * Divisional charts (D1, D2, D3, D4, D7, D9, D10, D12)
    * Vimshottari Mahadasha with sub-periods (Antardasha) and sub-sub-periods (Pratyantardasha)
    * Nakshatra calculations
    * Planetary aspects
    * Yoga (planetary combinations) detection
    """,
    version="1.0.0",
    docs_url="/v1/docs",
    redoc_url="/v1/redoc",
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load constants at startup
@app.on_event("startup")
async def startup_event():
    logger.info("Starting up JAI API")
    load_all_constants()
    # Initialize ephemeris
    from .services.ephemeris_service import init_ephemeris
    init_ephemeris()
    logger.info("Constants loaded and ephemeris initialized successfully")

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    logger.info("JAI API shutting down")
    # Close ephemeris
    from .services.ephemeris_service import close_ephemeris
    close_ephemeris()

# Add exception handlers
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    return await custom_exception_handler(request, exc)

# Include routers
app.include_router(health.router)
app.include_router(
    ascendant.router,
    prefix="/v1/api",
)
app.include_router(
    natal_chart.router,
    prefix="/v1/api",
)
app.include_router(
    divisional_chart.router,
    prefix="/v1/api",
)
app.include_router(
    mahadasha.router,
    prefix="/v1/api",
)
app.include_router(
    nakshatra.router,
    prefix="/v1/api",
)
app.include_router(
    aspect.router,
    prefix="/v1/api",
)
app.include_router(
    yoga.router,
    prefix="/v1/api",
)

@app.get("/", include_in_schema=False)
async def root():
    return {"message": "Welcome to JAI API. Visit /v1/docs for documentation."}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000) 