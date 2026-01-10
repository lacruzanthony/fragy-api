# Usa una versión "slim" (pequeña)
FROM python:3.11-slim

WORKDIR /app

# Instalar dependencias del sistema y limpiar caché de apt inmediatamente
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Gracias al .dockerignore, esto solo copiará tu código esencial
COPY . .

CMD ["gunicorn", "app.main:app", "--workers", "2", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8080"]