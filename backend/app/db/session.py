#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuração da sessão do banco de dados
"""

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.core.config import settings

# Criação do engine SQLAlchemy para conexão com o PostgreSQL
engine = create_engine(str(settings.DATABASE_URI))

# Fábrica de sessões para interação com o banco de dados
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Classe base para os modelos SQLAlchemy
Base = declarative_base()


def get_db():
    """
    Dependência para obter uma sessão do banco de dados.
    Garante que a sessão seja fechada após o uso.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def create_tables():
    """
    Cria todas as tabelas no banco de dados.
    """
    Base.metadata.create_all(bind=engine) 