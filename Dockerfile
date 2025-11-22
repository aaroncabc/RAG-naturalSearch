# /mnt/data/Dockerfile
FROM python:3.11-slim

# Evitar prompts y configurar locales (opcional)
ENV DEBIAN_FRONTEND=noninteractive

# Dependencias del sistema necesarias para algunas librerías ML y httpx
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    git \
    curl \
    ca-certificates \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements y fuente
COPY requirements.txt /app/requirements.txt
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--proxy-headers"]
