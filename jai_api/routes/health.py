from fastapi import APIRouter, status
from pydantic import BaseModel

# This will be imported from the ephemeris service later
def check_ephemeris_health():
    """Stub for ephemeris health check."""
    return True

router = APIRouter(tags=["Health"])

class HealthResponse(BaseModel):
    status: str
    version: str
    ephemeris: bool

@router.get(
    "/health",
    response_model=HealthResponse,
    status_code=status.HTTP_200_OK,
    summary="Health check endpoint"
)
async def health_check():
    """
    Health check endpoint for monitoring.
    Returns system status and version information.
    """
    # Check ephemeris health
    ephemeris_ok = check_ephemeris_health()
    
    return HealthResponse(
        status="ok",
        version="1.0.0",
        ephemeris=ephemeris_ok
    ) 