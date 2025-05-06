from fastapi import Request, status
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError

from .logger import get_logger
from .custom_exceptions import APIError

logger = get_logger(__name__)

async def custom_exception_handler(request: Request, exc: Exception):
    """
    Global exception handler for all API errors.
    
    Args:
        request: The request that caused the exception
        exc: The exception instance
        
    Returns:
        JSONResponse with appropriate error details
    """
    # Handle Pydantic validation errors
    if isinstance(exc, (RequestValidationError, PydanticValidationError)):
        errors = exc.errors()
        if errors:
            # Extract first error
            error_detail = errors[0]
            field = ".".join(str(loc) for loc in error_detail.get("loc", []))
            message = f"Invalid {field}: {error_detail.get('msg')}"
        else:
            message = "Validation error"
        
        logger.warning(f"Validation error: {message}")
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"error": {"code": 400, "message": message}}
        )
    
    # Handle custom API errors
    if isinstance(exc, APIError):
        logger.error(f"API error: {exc.message}")
        return JSONResponse(
            status_code=exc.status_code,
            content={"error": {"code": exc.status_code, "message": exc.message}}
        )
    
    # Handle unexpected errors
    logger.exception("Unexpected error")
    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "error": {
                "code": 500,
                "message": "Internal server error; please retry or contact support."
            }
        }
    ) 