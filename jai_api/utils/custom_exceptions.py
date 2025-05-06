class APIError(Exception):
    """Base class for API errors"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(self.message)

class ValidationError(APIError):
    """Raised when input validation fails"""
    def __init__(self, message: str):
        super().__init__(message, 400)

class CalculationError(APIError):
    """Raised when astrological calculation fails"""
    def __init__(self, message: str):
        super().__init__(message, 500)

class MappingNotFoundError(APIError):
    """Raised when a required divisional mapping is not available"""
    def __init__(self, chart: str):
        message = f"Divisional mapping for {chart} is not implemented"
        super().__init__(message, 500)

class EphemerisError(APIError):
    """Raised when there's an error with the ephemeris library"""
    def __init__(self, message: str):
        super().__init__(f"Ephemeris error: {message}", 500)

class TimeoutError(APIError):
    """Raised when a calculation times out"""
    def __init__(self, operation: str):
        message = f"Operation timed out: {operation}"
        super().__init__(message, 504) 