#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Endpoints para gerenciamento de pacientes
"""

from typing import Any, List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps
from app.db import models
from app.schemas import paciente as schemas

router = APIRouter()


@router.get("/")
async def listar_pacientes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Retorna a lista de pacientes.
    """
    # Por enquanto, retornamos uma resposta estática
    return {"message": "Endpoint para listar pacientes (placeholder)"}


@router.post("/")
async def criar_paciente(
    *,
    db: Session = Depends(deps.get_db),
):
    """
    Cria um novo paciente.
    """
    return {"message": "Endpoint para criar paciente (placeholder)"}


@router.get("/{paciente_id}")
async def ler_paciente(
    *,
    paciente_id: str,
    db: Session = Depends(deps.get_db),
):
    """
    Obtém um paciente por ID.
    """
    return {"message": f"Endpoint para ler paciente com ID {paciente_id} (placeholder)"}


@router.put("/{paciente_id}")
async def atualizar_paciente(
    *,
    paciente_id: str,
    db: Session = Depends(deps.get_db),
):
    """
    Atualiza um paciente.
    """
    return {"message": f"Endpoint para atualizar paciente com ID {paciente_id} (placeholder)"}


@router.delete("/{paciente_id}")
async def remover_paciente(
    *,
    paciente_id: str,
    db: Session = Depends(deps.get_db),
):
    """
    Remove um paciente.
    """
    return {"message": f"Endpoint para remover paciente com ID {paciente_id} (placeholder)"}


@router.get("/cpf/{cpf}")
async def ler_paciente_por_cpf(
    *,
    cpf: str,
    db: Session = Depends(deps.get_db),
):
    """
    Obtém um paciente por CPF.
    """
    return {"message": f"Endpoint para ler paciente com CPF {cpf} (placeholder)"}


@router.get("/sus/{sus_numero}")
async def ler_paciente_por_sus(
    *,
    sus_numero: str,
    db: Session = Depends(deps.get_db),
):
    """
    Obtém um paciente por número do SUS.
    """
    return {"message": f"Endpoint para ler paciente com número SUS {sus_numero} (placeholder)"} 