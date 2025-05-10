"""
Main entry point to run the JAI API

This is the only entry point to the application.
It creates the app from the api.main module and runs it with uvicorn.
"""
import uvicorn
import os
from api.main import create_app

# Create the application
app = create_app()

if __name__ == "__main__":
    # Get port from environment or use default
    port = int(os.environ.get("PORT", "8000"))
    
    # Start the server
    uvicorn.run(
        "run:app", 
        host="0.0.0.0", 
        port=port, 
        reload=True if os.environ.get("ENV") == "development" else False
    ) 