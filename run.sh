#!/bin/bash

# ----------------------------------------
# Script para ejecutar el microservicio RAG
# ----------------------------------------

# Cargar variables desde archivo .env si existe
if [ -f ".env" ]; then
    echo "Cargando variables desde .env..."
    export $(grep -v '^#' .env | xargs)
fi

echo "Iniciando servicio RAG..."
echo "Host: 0.0.0.0"
echo "Puerto: 8000"

# Ejecutar uvicorn
uvicorn app.main:app \
    --host 0.0.0.0 \
    --port 8000 \
    --proxy-headers \
    --forwarded-allow-ips="*" \
    "$@"
