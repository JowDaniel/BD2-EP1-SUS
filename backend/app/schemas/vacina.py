#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Schemas Pydantic para validação e serialização de dados de Vacina
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, Field


class VacinaBase(BaseModel):
    """
    Atributos comuns a todas as representações de Vacina
    """
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    fabricante: Optional[str] = Field(None, max_length=100)
    lote: Optional[str] = Field(None, max_length=50)
    validade: Optional[date] = None


class VacinaCreate(VacinaBase):
    """
    Atributos necessários para criar uma nova Vacina
    """
    nome: str = Field(..., min_length=2, max_length=100)
    fabricante: str = Field(..., max_length=100)
    lote: str = Field(..., max_length=50)
    validade: date


class VacinaUpdate(VacinaBase):
    """
    Atributos que podem ser atualizados em uma Vacina
    """
    pass


class VacinaInDBBase(VacinaBase):
    """
    Atributos presentes em modelos armazenados no banco de dados
    """
    vacina_id: UUID
    data_cadastro: datetime

    class Config:
        from_attributes = True


class Vacina(VacinaInDBBase):
    """
    Schema completo para retorno ao cliente
    """
    pass 