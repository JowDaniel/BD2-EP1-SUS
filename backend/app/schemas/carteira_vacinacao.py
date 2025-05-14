#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Schemas Pydantic para validação e serialização de dados da Carteira de Vacinação
"""

from datetime import datetime
from typing import Optional, List
from uuid import UUID

from pydantic import BaseModel, Field

from app.schemas.paciente import Paciente
from app.schemas.vacina import Vacina


class CarteiraVacinacaoBase(BaseModel):
    """
    Atributos comuns a todas as representações de Carteira de Vacinação
    """
    paciente_id: Optional[UUID] = None
    vacina_id: Optional[UUID] = None
    funcionario_id: Optional[UUID] = None
    estabelecimento_id: Optional[UUID] = None
    data_aplicacao: Optional[datetime] = None
    dose: Optional[str] = Field(None, max_length=20)
    observacoes: Optional[str] = None


class CarteiraVacinacaoCreate(BaseModel):
    """
    Atributos necessários para criar um novo registro de vacinação
    """
    paciente_id: UUID
    vacina_id: UUID
    funcionario_id: UUID
    estabelecimento_id: UUID
    data_aplicacao: datetime
    dose: str = Field(..., max_length=20)
    observacoes: Optional[str] = None


class CarteiraVacinacaoUpdate(BaseModel):
    """
    Atributos que podem ser atualizados em um registro de vacinação
    """
    observacoes: Optional[str] = None


class CarteiraVacinacaoInDBBase(CarteiraVacinacaoBase):
    """
    Atributos presentes em modelos armazenados no banco de dados
    """
    vacinacao_id: UUID
    data_cadastro: datetime

    class Config:
        from_attributes = True


class CarteiraVacinacao(CarteiraVacinacaoInDBBase):
    """
    Schema completo para retorno ao cliente
    """
    pass


class CarteiraVacinacaoCompleta(CarteiraVacinacao):
    """
    Schema para carteira de vacinação com dados relacionados
    """
    nome_paciente: str
    nome_vacina: str
    nome_estabelecimento: str
    tipo_estabelecimento: str
    nome_funcionario: str

    class Config:
        from_attributes = False


class CarteiraVacinacaoPaciente(BaseModel):
    """
    Schema para retornar todas as vacinas de um paciente
    """
    paciente: Paciente
    vacinacoes: List[CarteiraVacinacaoCompleta]

    class Config:
        from_attributes = False 