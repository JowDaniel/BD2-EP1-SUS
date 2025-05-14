#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Aplicação principal do Sistema de Compartilhamento de Dados de Pacientes do SUS
"""

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import settings
from app.api.api import api_router
from app.db.session import create_tables

# Inicialização da aplicação FastAPI
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="API para o Sistema de Compartilhamento de Dados de Pacientes do SUS",
    version="0.1.0",
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configuração do CORS para permitir comunicação com o frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclusão dos endpoints da API
app.include_router(api_router, prefix=settings.API_V1_STR)

# Evento de inicialização da aplicação
@app.on_event("startup")
async def startup_event():
    """
    Executa ações necessárias na inicialização da aplicação
    """
    create_tables()


# Rota raiz para verificação de saúde da API
@app.get("/")
async def health_check():
    """
    Endpoint para verificar se a API está online
    """
    return {
        "status": "online",
        "message": "Sistema de Compartilhamento de Dados de Pacientes do SUS - API online",
    }


# Execução da aplicação em modo de desenvolvimento
if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info",
    ) 