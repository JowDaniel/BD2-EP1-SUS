#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Schemas Pydantic para validação e serialização de dados de Estabelecimento
"""

from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator


class EstabelecimentoBase(BaseModel):
    """
    Atributos comuns a todas as representações de Estabelecimento
    """
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    tipo: Optional[str] = Field(None, pattern="^(POSTO|HOSPITAL|UPA|OUTRO)$")
    cnes: Optional[str] = Field(None, min_length=7, max_length=20)
    endereco: Optional[str] = Field(None, max_length=200)
    telefone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    horario_funcionamento: Optional[str] = Field(None, max_length=100)


class EstabelecimentoCreate(EstabelecimentoBase):
    """
    Atributos necessários para criar um novo Estabelecimento
    """
    nome: str = Field(..., min_length=2, max_length=100)
    tipo: str = Field(..., pattern="^(POSTO|HOSPITAL|UPA|OUTRO)$")
    cnes: str = Field(..., min_length=7, max_length=20)
    endereco: str = Field(..., max_length=200)

    @validator('cnes')
    def validar_cnes(cls, v):
        """
        Valida o formato do CNES (simplificado)
        """
        # Remove caracteres não numéricos
        cnes = ''.join(filter(str.isdigit, v))
        if len(cnes) < 7:
            raise ValueError('CNES deve conter no mínimo 7 dígitos')
        return v


class EstabelecimentoUpdate(EstabelecimentoBase):
    """
    Atributos que podem ser atualizados em um Estabelecimento
    """
    pass


class EstabelecimentoInDBBase(EstabelecimentoBase):
    """
    Atributos presentes em modelos armazenados no banco de dados
    """
    estabelecimento_id: UUID
    data_cadastro: datetime
    ultima_atualizacao: datetime

    class Config:
        from_attributes = True


class Estabelecimento(EstabelecimentoInDBBase):
    """
    Schema completo para retorno ao cliente
    """
    pass


class EstabelecimentoList(BaseModel):
    """
    Schema para listagem simplificada de estabelecimentos
    """
    estabelecimento_id: UUID
    nome: str
    tipo: str
    endereco: str
    telefone: Optional[str] = None
    horario_funcionamento: Optional[str] = None

    class Config:
        from_attributes = True 