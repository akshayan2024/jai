"""
Main entry point to run the JAI API
"""
import uvicorn
from api.main import create_app

app = create_app()

if __name__ == "__main__":
    uvicorn.run(
        "run:app", 
        host="0.0.0.0", 
        port=8000, 
        reload=True
    ) 