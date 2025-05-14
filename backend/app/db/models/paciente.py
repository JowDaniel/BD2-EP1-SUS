#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo SQLAlchemy para Paciente
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, Date, DateTime, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID

from app.db.session import Base


class Paciente(Base):
    """
    Modelo de Paciente correspondente à tabela 'pacientes' no banco de dados
    """
    __tablename__ = "pacientes"

    # Campos correspondentes à tabela no banco de dados
    paciente_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    nome = Column(String(100), nullable=False)
    cpf = Column(String(14), unique=True, nullable=False)
    data_nascimento = Column(Date, nullable=False)
    sexo = Column(String(1), CheckConstraint("sexo IN ('M', 'F', 'O')"))
    endereco = Column(String(200))
    telefone = Column(String(20))
    email = Column(String(100))
    tipo_sanguineo = Column(String(3))
    sus_numero = Column(String(20), unique=True, nullable=False)
    data_cadastro = Column(DateTime, default=datetime.now)
    ultima_atualizacao = Column(DateTime, default=datetime.now, onupdate=datetime.now)

    def __repr__(self):
        return f"<Paciente(nome='{self.nome}', cpf='{self.cpf}', sus_numero='{self.sus_numero}')>" 