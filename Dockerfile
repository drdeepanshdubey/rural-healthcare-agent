# Use official Python runtime as base image
FROM python:3.12-slim

# Set working directory in container
WORKDIR /app

# Copy requirements file first (for better caching)
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy all project files to container
COPY . .

# Set environment variable for port
ENV PORT=8080

# Expose port 8080 for the Flask app
EXPOSE 8080

# Command to run the Flask application
CMD ["python", "app.py"]
