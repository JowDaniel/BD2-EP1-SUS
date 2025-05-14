#!/bin/bash
set -e

# Esperando o PostgreSQL iniciar
echo "Esperando o PostgreSQL iniciar..."
while ! pg_isready -h postgres -p 5432 -U postgres; do
  sleep 1
done

echo "PostgreSQL iniciado, configurando o banco de dados..."

# Criar banco de dados (se não existir)
PGPASSWORD=postgres psql -v ON_ERROR_STOP=0 -h postgres -U postgres <<-EOSQL
    SELECT 'CREATE DATABASE sus_db WITH OWNER postgres' WHERE NOT EXISTS (SELECT FROM pg_database WHERE datname = 'sus_db')\gexec
EOSQL

# Executar scripts de schema
echo "Aplicando schema..."
PGPASSWORD=postgres psql -v ON_ERROR_STOP=1 -h postgres -U postgres -d sus_db -f /sql/ddl/schema.sql

# Executar scripts de dados de exemplo
echo "Inserindo dados de exemplo..."
PGPASSWORD=postgres psql -v ON_ERROR_STOP=1 -h postgres -U postgres -d sus_db -f /sql/dml/sample_data.sql

echo "Banco de dados configurado com sucesso!" 