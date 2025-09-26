# Stage 1: Base Image & Core Dependencies
# Using a specific slim Python version is a best practice for security and stability.
FROM python:3.11-slim

# Set environment variables for Python
# 1. Prevents Python from buffering stdout and stderr, ensuring logs appear in real-time.
# 2. Prevents Python from writing .pyc files, which aren't needed in a container.
ENV PYTHONUNBUFFERED 1
ENV PYTHONDONTWRITEBYTECODE 1

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies
# - netcat-openbsd: For the database health check.
# - WeasyPrint dependencies: For PDF generation capabilities.
# - Clean up apt cache in the same layer to reduce image size.
RUN apt-get update && \
    apt-get install -y \
    netcat-openbsd \
    libpango-1.0-0 \
    libpangoft2-1.0-0 \
    libgobject-2.0-0 \
    libffi-dev \
    libcairo2 \
    gdk-pixbuf2.0-0 \
    shared-mime-info \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
# First, copy only the requirements file to leverage Docker's build cache.
# This layer is only rebuilt if the requirements.txt file changes.
COPY mysite/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire application source code into the container
COPY . .

# Expose the port the app runs on.
EXPOSE 8000
