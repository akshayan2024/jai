# Use Python 3.9 slim as base image
FROM python:3.9-slim as builder

# Set working directory
WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file
COPY requirements.txt .

# Build wheels
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.9-slim as api

# Create non-root user
RUN useradd -m appuser

# Set working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    python3-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder
COPY --from=builder /app/wheels /app/wheels

# Install Python packages
RUN pip install --no-cache-dir /app/wheels/*

# Install pyswisseph directly from PyPI
RUN pip install --no-cache-dir --no-binary :all: pyswisseph==2.10.3.2

# Copy application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV EPHEMERIS_PATH=/usr/local/lib/python3.9/site-packages/pyswisseph/ephe
ENV ENV=production

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the application
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"] 