#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo SQLAlchemy para Vacina
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Date, DateTime
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class Vacina(Base):
    """
    Modelo de Vacina correspondente à tabela 'vacinas' no banco de dados
    """
    __tablename__ = "vacinas"

    # Campos correspondentes à tabela no banco de dados
    vacina_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False)
    fabricante = Column(String(100))
    lote = Column(String(50))
    validade = Column(Date)
    data_cadastro = Column(DateTime, default=datetime.now)

    def __repr__(self):
        return f"<Vacina(nome='{self.nome}', fabricante='{self.fabricante}', lote='{self.lote}')>" 