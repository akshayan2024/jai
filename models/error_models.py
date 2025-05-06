from typing import Dict, Union
from pydantic import BaseModel

class ErrorResponse(BaseModel):
    """Standard error response model"""
    error: Dict[str, Union[int, str]] = {
        "code": 400,
        "message": "Bad Request"
    } 