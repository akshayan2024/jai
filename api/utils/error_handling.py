"""
Standardized error handling for JAI API
Ensures consistent error responses that are easily parseable by GPT
"""
from fastapi import HTTPException, Request
from fastapi.responses import JSONResponse
from fastapi.exception_handlers import http_exception_handler
from datetime import datetime
from typing import Dict, Any, Optional
import logging

# Configure logger
logger = logging.getLogger("jai_api")

# Error code constants
class ErrorCode:
    INVALID_DATE_FORMAT = "INVALID_DATE_FORMAT"
    INVALID_TIME_FORMAT = "INVALID_TIME_FORMAT"
    GEOCODING_ERROR = "GEOCODING_ERROR"
    MISSING_LOCATION = "MISSING_LOCATION"
    MISSING_PARAMETERS = "MISSING_PARAMETERS"
    CALCULATION_ERROR = "CALCULATION_ERROR"
    EPHEMERIS_ERROR = "EPHEMERIS_ERROR"
    TIMEZONE_ERROR = "TIMEZONE_ERROR"
    INTERNAL_SERVER_ERROR = "INTERNAL_SERVER_ERROR"
    VALIDATION_ERROR = "VALIDATION_ERROR"
    RATE_LIMIT_EXCEEDED = "RATE_LIMIT_EXCEEDED"

class APIError(Exception):
    """Custom API error with code, message, and details"""
    def __init__(
        self, 
        status_code: int, 
        error_code: str, 
        message: str, 
        details: Optional[Dict[str, Any]] = None
    ):
        self.status_code = status_code
        self.error_code = error_code
        self.message = message
        self.details = details
        super().__init__(self.message)

async def api_error_handler(request: Request, exc: APIError) -> JSONResponse:
    """Handler for APIError exceptions"""
    # Log the error with appropriate level based on status code
    if exc.status_code >= 500:
        logger.error(
            f"Internal error: {exc.message}",
            extra={"error_code": exc.error_code, "details": exc.details}
        )
    else:
        logger.warning(
            f"Client error: {exc.message}",
            extra={"error_code": exc.error_code, "details": exc.details}
        )
    
    # Build standardized error response
    content = {
        "status": "error",
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "error_code": exc.error_code,
        "error_message": exc.message
    }
    
    # Add request parameters if available
    try:
        body = await request.json()
        content["request_params"] = body
    except Exception:
        # If request body can't be parsed, don't include it
        pass
    
    # Add error details if provided
    if exc.details:
        content["error_details"] = exc.details
    
    return JSONResponse(
        status_code=exc.status_code,
        content=content
    )

async def http_exception_with_details(request: Request, exc: HTTPException) -> JSONResponse:
    """Enhanced HTTP exception handler with standardized format"""
    # Log the error
    logger.warning(f"HTTP exception: {exc.detail}")
    
    # Check if detail is already a dict with our format
    if isinstance(exc.detail, dict) and "error_code" in exc.detail:
        return JSONResponse(
            status_code=exc.status_code,
            content=exc.detail
        )
    
    # Create standardized error response
    content = {
        "status": "error",
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "error_code": "HTTP_ERROR",
        "error_message": str(exc.detail)
    }
    
    # Add request parameters if available
    try:
        body = await request.json()
        content["request_params"] = body
    except Exception:
        # If request body can't be parsed, don't include it
        pass
    
    return JSONResponse(
        status_code=exc.status_code,
        content=content
    )

async def validation_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Handler for pydantic validation errors"""
    # Log the error
    logger.warning(f"Validation error: {str(exc)}")
    
    # Extract validation error details
    details = {"validation_errors": []}
    if hasattr(exc, "errors") and callable(getattr(exc, "errors")):
        for error in exc.errors():
            details["validation_errors"].append({
                "loc": error.get("loc", []),
                "msg": error.get("msg", ""),
                "type": error.get("type", "")
            })
    
    # Create standardized error response
    content = {
        "status": "error",
        "version": "1.0",
        "generated_at": datetime.now().isoformat(),
        "error_code": ErrorCode.VALIDATION_ERROR,
        "error_message": "Invalid request parameters",
        "error_details": details
    }
    
    # Add request parameters if available
    try:
        body = await request.json()
        content["request_params"] = body
    except Exception:
        # If request body can't be parsed, don't include it
        pass
    
    return JSONResponse(
        status_code=422,
        content=content
    )

def get_error_handlers():
    """Return dictionary of exception handlers to register with FastAPI"""
    return {
        APIError: api_error_handler,
        HTTPException: http_exception_with_details
    }

# Helper functions for common errors
def raise_validation_error(message: str, param: str, value: Any) -> None:
    """Raise a validation error with standardized format"""
    raise APIError(
        status_code=400,
        error_code=ErrorCode.VALIDATION_ERROR,
        message=message,
        details={
            "parameter": param,
            "received_value": value
        }
    )

def raise_missing_parameter_error(param: str) -> None:
    """Raise an error for missing required parameter"""
    raise APIError(
        status_code=400,
        error_code=ErrorCode.MISSING_PARAMETERS,
        message=f"Missing required parameter: {param}"
    )

def raise_geocoding_error(place: str, error_message: str) -> None:
    """Raise an error when geocoding fails"""
    raise APIError(
        status_code=400,
        error_code=ErrorCode.GEOCODING_ERROR,
        message=f"Could not geocode place: {place}",
        details={
            "place": place,
            "error": error_message
        }
    ) 