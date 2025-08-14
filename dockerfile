# Use Python 3.9 base image for better compatibility
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better Docker layer caching
COPY requirements.txt .

# Upgrade pip and install dependencies
RUN pip install --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy all application files
COPY . .

# Expose port
EXPOSE 8000

# Command to start FastAPI application
CMD ["uvicorn", "app1:app", "--host", "0.0.0.0", "--port", "8000"]
