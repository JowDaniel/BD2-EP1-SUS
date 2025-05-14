#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Schemas Pydantic para validação e serialização de dados de Paciente
"""

from datetime import date, datetime
from typing import Optional
from uuid import UUID

from pydantic import BaseModel, EmailStr, Field, validator


class PacienteBase(BaseModel):
    """
    Atributos comuns a todas as representações de Paciente
    """
    nome: Optional[str] = Field(None, min_length=2, max_length=100)
    cpf: Optional[str] = Field(None, min_length=11, max_length=14)
    data_nascimento: Optional[date] = None
    sexo: Optional[str] = Field(None, pattern="^[MFO]$")
    endereco: Optional[str] = Field(None, max_length=200)
    telefone: Optional[str] = Field(None, max_length=20)
    email: Optional[EmailStr] = None
    tipo_sanguineo: Optional[str] = Field(None, max_length=3)
    sus_numero: Optional[str] = Field(None, min_length=15, max_length=20)


class PacienteCreate(PacienteBase):
    """
    Atributos necessários para criar um novo Paciente
    """
    nome: str = Field(..., min_length=2, max_length=100)
    cpf: str = Field(..., min_length=11, max_length=14)
    data_nascimento: date
    sexo: str = Field(..., pattern="^[MFO]$")
    sus_numero: str = Field(..., min_length=15, max_length=20)

    @validator('cpf')
    def validar_cpf(cls, v):
        """
        Valida o formato do CPF (simplificado)
        """
        # Remove caracteres não numéricos
        cpf = ''.join(filter(str.isdigit, v))
        if len(cpf) != 11:
            raise ValueError('CPF deve conter 11 dígitos')
        return v

    @validator('sus_numero')
    def validar_sus(cls, v):
        """
        Valida o formato do número do SUS (simplificado)
        """
        # Remove caracteres não numéricos
        sus = ''.join(filter(str.isdigit, v))
        if len(sus) != 15:
            raise ValueError('Número do SUS deve conter 15 dígitos')
        return v


class PacienteUpdate(PacienteBase):
    """
    Atributos que podem ser atualizados em um Paciente
    """
    pass


class PacienteInDBBase(PacienteBase):
    """
    Atributos presentes em modelos armazenados no banco de dados
    """
    paciente_id: UUID
    data_cadastro: datetime
    ultima_atualizacao: datetime

    class Config:
        from_attributes = True


class Paciente(PacienteInDBBase):
    """
    Schema completo para retorno ao cliente
    """
    pass 