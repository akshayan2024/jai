# Build stage
FROM python:3.9-slim as builder

WORKDIR /app

# Install build dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    gcc \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt .
RUN pip wheel --no-cache-dir --wheel-dir /app/wheels -r requirements.txt

# Final stage
FROM python:3.9-slim

# Create non-root user
RUN useradd -m appuser

WORKDIR /app

# Install runtime dependencies for Swiss Ephemeris
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgomp1 \
    python3-dev \
    gcc \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy wheels from builder stage
COPY --from=builder /app/wheels /app/wheels
RUN pip install --no-cache-dir /app/wheels/*

# Install pyswisseph directly
RUN pip install --no-cache-dir pyswisseph==2.10.3.2

# Copy application code
COPY . .

# Create ephemeris directory and ensure it exists
RUN mkdir -p /app/ephemeris

# Copy ephemeris files from local directory
# The files should be downloaded first using download_ephemeris.sh
COPY ./ephemeris/* /app/ephemeris/

# Change ownership to non-root user
RUN chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose API port
EXPOSE 8000

# Start application
CMD ["uvicorn", "run:app", "--host", "0.0.0.0", "--port", "8000"] 