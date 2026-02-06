FROM python:3.10-slim

WORKDIR /app

# Install system dependencies for psycopg2
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    postgresql-client \
    && rm -rf /var/lib/apt/lists/*

# Copy the backend requirements first
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

WORKDIR /app/backend

EXPOSE 7860

# Use the production server which handles Hugging Face deployment better
CMD ["python", "/app/backend/prod_server.py"]