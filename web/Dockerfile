# syntax=docker/dockerfile:1
FROM python:3.12-slim AS base

# Install system deps for psycopg2 and build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential libpq-dev \
 && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Install python deps (paths relative to the build context ./web)
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

# Copy the application source (everything from ./web)
COPY . /app/

# Create non-root user
RUN useradd -m appuser && chown -R appuser:appuser /app
USER appuser

# Expose gunicorn port
EXPOSE 8000

# Start gunicorn
CMD ["gunicorn", "app:create_app()", "-b", "0.0.0.0:8000", "-w", "3", "--timeout", "60"]
