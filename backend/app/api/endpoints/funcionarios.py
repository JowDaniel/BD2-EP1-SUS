#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Endpoints para gerenciamento de funcionários
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.api import deps

router = APIRouter()


@router.get("/")
async def listar_funcionarios(
    db: Session = Depends(deps.get_db),
):
    """
    Endpoint placeholder para listar funcionários
    """
    return {"message": "Endpoint para listar funcionários (placeholder)"} 