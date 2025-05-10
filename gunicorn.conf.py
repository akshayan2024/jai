"""
Gunicorn configuration for JAI API deployment
"""
import os

# Bind to the PORT provided by the environment
bind = f"0.0.0.0:{os.environ.get('PORT', '8000')}"

# Worker configuration
workers = 2
worker_class = "uvicorn.workers.UvicornWorker"
preload_app = True

# Timeout configuration
timeout = 120
keepalive = 5

# Logging
accesslog = "-"  # Log to stdout
errorlog = "-"   # Log to stderr
loglevel = "info"

# Run our application from run.py
wsgi_app = "run:app" 