#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo SQLAlchemy para Estabelecimento
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class Estabelecimento(Base):
    """
    Modelo de Estabelecimento correspondente à tabela 'estabelecimentos' no banco de dados
    """
    __tablename__ = "estabelecimentos"

    # Campos correspondentes à tabela no banco de dados
    estabelecimento_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False)
    tipo = Column(String(50), CheckConstraint("tipo IN ('POSTO', 'HOSPITAL', 'UPA', 'OUTRO')"), nullable=False)
    cnes = Column(String(20), unique=True, nullable=False)
    endereco = Column(String(200), nullable=False)
    telefone = Column(String(20))
    email = Column(String(100))
    horario_funcionamento = Column(String(100))
    data_cadastro = Column(DateTime, default=datetime.now)
    ultima_atualizacao = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Estabelecimento(nome='{self.nome}', tipo='{self.tipo}', cnes='{self.cnes}')>" 