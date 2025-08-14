# Use Python 3.11 base image
FROM python:3.11-slim


WORKDIR /app1


COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


COPY . .


EXPOSE 8000

# Command to start FastAPI application
CMD ["uvicorn", "app1:app", "--host", "0.0.0.0", "--port", "8000"]