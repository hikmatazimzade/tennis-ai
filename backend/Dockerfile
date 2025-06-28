FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for ML libraries
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN pip install --no-cache-dir uv

# Copy everything to maintain the exact structure
COPY . .

# Remove uv.lock to regenerate for Linux platform
RUN rm -f uv.lock

# Install dependencies using uv (will generate Linux-compatible lock)
RUN uv sync --no-install-project

# Set PYTHONPATH to include root directory
ENV PYTHONPATH=/app

# Expose port
EXPOSE 8000

# Run the application from root directory exactly as you would locally
CMD ["uv", "run", "--no-project", "uvicorn", "backend.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]