#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo SQLAlchemy para Funcionário
"""

import uuid
from datetime import datetime, date

from sqlalchemy import Column, String, Date, DateTime, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base


class Funcionario(Base):
    """
    Modelo de Funcionário correspondente à tabela 'funcionarios' no banco de dados
    """
    __tablename__ = "funcionarios"

    # Campos correspondentes à tabela no banco de dados
    funcionario_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    estabelecimento_id = Column(UUID(as_uuid=True), ForeignKey("estabelecimentos.estabelecimento_id"), nullable=False)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    cargo = Column(String(50), nullable=False)
    registro_profissional = Column(String(20))
    data_contratacao = Column(Date, nullable=False)
    telefone = Column(String(20))
    email = Column(String(100))
    ativo = Column(Boolean, default=True)
    data_cadastro = Column(DateTime, default=datetime.now)
    ultima_atualizacao = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    # Relacionamentos
    estabelecimento = relationship("Estabelecimento", backref="funcionarios")

    def __repr__(self):
        return f"<Funcionario(nome='{self.nome}', cargo='{self.cargo}', registro='{self.registro_profissional}')>" 