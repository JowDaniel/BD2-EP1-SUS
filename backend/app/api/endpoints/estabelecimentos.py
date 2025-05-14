#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Endpoints para gerenciamento de estabelecimentos
"""

from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session

from app.api import deps
from app.db.models.estabelecimento import Estabelecimento
from app.schemas import estabelecimento as schemas

router = APIRouter()


@router.get("/", response_model=List[schemas.EstabelecimentoList])
async def listar_estabelecimentos(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    tipo: Optional[str] = Query(None, description="Filtrar por tipo (POSTO, HOSPITAL, UPA, OUTRO)")
):
    """
    Retorna a lista de estabelecimentos de saúde.
    Opcionalmente filtra por tipo.
    """
    query = db.query(Estabelecimento)
    
    if tipo:
        query = query.filter(Estabelecimento.tipo == tipo)
    
    estabelecimentos = query.offset(skip).limit(limit).all()
    return estabelecimentos


@router.get("/{estabelecimento_id}", response_model=schemas.Estabelecimento)
async def ler_estabelecimento(
    estabelecimento_id: str,
    db: Session = Depends(deps.get_db)
):
    """
    Obtém um estabelecimento pelo ID.
    """
    estabelecimento = db.query(Estabelecimento).filter(Estabelecimento.estabelecimento_id == estabelecimento_id).first()
    if not estabelecimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estabelecimento não encontrado"
        )
    return estabelecimento


@router.post("/", response_model=schemas.Estabelecimento, status_code=status.HTTP_201_CREATED)
async def criar_estabelecimento(
    estabelecimento_in: schemas.EstabelecimentoCreate,
    db: Session = Depends(deps.get_db)
):
    """
    Cria um novo estabelecimento de saúde.
    """
    # Verificar se já existe estabelecimento com o mesmo CNES
    db_estabelecimento = db.query(Estabelecimento).filter(Estabelecimento.cnes == estabelecimento_in.cnes).first()
    if db_estabelecimento:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Já existe um estabelecimento com este CNES"
        )
    
    # Criar novo estabelecimento
    novo_estabelecimento = Estabelecimento(
        nome=estabelecimento_in.nome,
        tipo=estabelecimento_in.tipo,
        cnes=estabelecimento_in.cnes,
        endereco=estabelecimento_in.endereco,
        telefone=estabelecimento_in.telefone,
        email=estabelecimento_in.email,
        horario_funcionamento=estabelecimento_in.horario_funcionamento
    )
    
    db.add(novo_estabelecimento)
    db.commit()
    db.refresh(novo_estabelecimento)
    
    return novo_estabelecimento


@router.put("/{estabelecimento_id}", response_model=schemas.Estabelecimento)
async def atualizar_estabelecimento(
    estabelecimento_id: str,
    estabelecimento_in: schemas.EstabelecimentoUpdate,
    db: Session = Depends(deps.get_db)
):
    """
    Atualiza um estabelecimento de saúde.
    """
    estabelecimento = db.query(Estabelecimento).filter(Estabelecimento.estabelecimento_id == estabelecimento_id).first()
    if not estabelecimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estabelecimento não encontrado"
        )
    
    # Atualizar campos
    update_data = estabelecimento_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(estabelecimento, key, value)
    
    db.add(estabelecimento)
    db.commit()
    db.refresh(estabelecimento)
    
    return estabelecimento


@router.delete("/{estabelecimento_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_estabelecimento(
    estabelecimento_id: str,
    db: Session = Depends(deps.get_db)
):
    """
    Remove um estabelecimento de saúde.
    """
    estabelecimento = db.query(Estabelecimento).filter(Estabelecimento.estabelecimento_id == estabelecimento_id).first()
    if not estabelecimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estabelecimento não encontrado"
        )
    
    db.delete(estabelecimento)
    db.commit()
    
    return None


@router.get("/tipo/{tipo}", response_model=List[schemas.EstabelecimentoList])
async def listar_estabelecimentos_por_tipo(
    tipo: str,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100
):
    """
    Retorna a lista de estabelecimentos de saúde por tipo específico.
    Tipos: POSTO, HOSPITAL, UPA, OUTRO
    """
    if tipo not in ["POSTO", "HOSPITAL", "UPA", "OUTRO"]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Tipo de estabelecimento inválido. Use POSTO, HOSPITAL, UPA ou OUTRO"
        )
    
    estabelecimentos = db.query(Estabelecimento).filter(Estabelecimento.tipo == tipo).offset(skip).limit(limit).all()
    return estabelecimentos 