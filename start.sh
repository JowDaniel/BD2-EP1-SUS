#!/bin/bash
echo "Parando containers anteriores..."
docker compose down

echo "Removendo volumes antigos..."
docker volume rm ep1_postgres_data || true

echo "Reconstruindo as imagens..."
docker compose build --no-cache

echo "Iniciando o sistema..."
docker compose up 