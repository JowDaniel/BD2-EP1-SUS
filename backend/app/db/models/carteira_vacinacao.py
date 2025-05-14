#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Modelo SQLAlchemy para Carteira de Vacinação
"""

import uuid
from datetime import datetime

from sqlalchemy import Column, String, DateTime, Text, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.session import Base


class CarteiraVacinacao(Base):
    """
    Modelo de Carteira de Vacinação correspondente à tabela 'carteira_vacinacao' no banco de dados
    """
    __tablename__ = "carteira_vacinacao"

    # Campos correspondentes à tabela no banco de dados
    vacinacao_id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    paciente_id = Column(UUID(as_uuid=True), ForeignKey("pacientes.paciente_id"), nullable=False)
    vacina_id = Column(UUID(as_uuid=True), ForeignKey("vacinas.vacina_id"), nullable=False)
    funcionario_id = Column(UUID(as_uuid=True), ForeignKey("funcionarios.funcionario_id"), nullable=False)
    estabelecimento_id = Column(UUID(as_uuid=True), ForeignKey("estabelecimentos.estabelecimento_id"), nullable=False)
    data_aplicacao = Column(DateTime, nullable=False)
    dose = Column(String(20), nullable=False)
    observacoes = Column(Text)
    data_cadastro = Column(DateTime, default=datetime.now)

    # Relacionamentos (caso precise acessar os objetos relacionados)
    paciente = relationship("Paciente", backref="vacinacoes")
    vacina = relationship("Vacina", backref="aplicacoes")
    funcionario = relationship("Funcionario", backref="vacinacoes_aplicadas")
    estabelecimento = relationship("Estabelecimento", backref="vacinacoes_realizadas")

    def __repr__(self):
        return f"<CarteiraVacinacao(paciente_id='{self.paciente_id}', vacina_id='{self.vacina_id}', dose='{self.dose}')>" 