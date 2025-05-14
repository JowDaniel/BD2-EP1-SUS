#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configurações da aplicação
"""

import os
import secrets
from typing import Any, Dict, List, Optional, Union

from pydantic import (
    AnyHttpUrl,
    PostgresDsn,
    validator,
)
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """
    Configurações do aplicativo usando Pydantic para validação
    e tratamento de variáveis de ambiente.
    """
    
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str = secrets.token_urlsafe(32)
    # 60 minutes * 24 hours * 8 days = 8 days
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8
    
    # Nome do projeto
    PROJECT_NAME: str = "Sistema de Compartilhamento de Dados de Pacientes do SUS"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []
    
    # PostgreSQL
    POSTGRES_SERVER: str = os.getenv("POSTGRES_SERVER", "localhost")
    POSTGRES_USER: str = os.getenv("POSTGRES_USER", "postgres")
    POSTGRES_PASSWORD: str = os.getenv("POSTGRES_PASSWORD", "postgres")
    POSTGRES_DB: str = os.getenv("POSTGRES_DB", "sus_db")
    POSTGRES_PORT: str = os.getenv("POSTGRES_PORT", "5432")
    DATABASE_URI: Optional[PostgresDsn] = None
    
    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """
        Valida e formata a configuração de CORS.
        """
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @validator("DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        """
        Constrói a string de conexão com o banco de dados.
        """
        if isinstance(v, str):
            return v
        
        server = values.get("POSTGRES_SERVER")
        user = values.get("POSTGRES_USER")
        password = values.get("POSTGRES_PASSWORD")
        db = values.get("POSTGRES_DB")
        port = values.get("POSTGRES_PORT")
        
        # Se a porta for uma string vazia, use a porta padrão 5432
        if not port:
            port = "5432"
            
        # Constrói a DSN do PostgreSQL
        return f"postgresql://{user}:{password}@{server}:{port}/{db}"
    
    class Config:
        env_file = ".env"
        case_sensitive = True


# Instância das configurações para uso no aplicativo
settings = Settings() 