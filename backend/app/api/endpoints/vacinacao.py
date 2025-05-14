#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Endpoints para gerenciamento de vacinação
"""

from typing import List, Optional
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import and_

from app.api import deps
from app.db.models.vacina import Vacina
from app.db.models.carteira_vacinacao import CarteiraVacinacao
from app.db.models.paciente import Paciente
from app.db.models.estabelecimento import Estabelecimento
from app.db.models.funcionario import Funcionario
from app.schemas import vacina as vacina_schemas
from app.schemas import carteira_vacinacao as vacinacao_schemas

router = APIRouter()

# ENDPOINTS PARA VACINAS

@router.get("/vacinas/", response_model=List[vacina_schemas.Vacina])
async def listar_vacinas(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    nome: Optional[str] = Query(None, description="Filtrar por nome da vacina"),
    fabricante: Optional[str] = Query(None, description="Filtrar por fabricante")
):
    """
    Retorna a lista de vacinas disponíveis.
    Opcionalmente filtra por nome ou fabricante.
    """
    query = db.query(Vacina)
    
    if nome:
        query = query.filter(Vacina.nome.ilike(f"%{nome}%"))
    
    if fabricante:
        query = query.filter(Vacina.fabricante.ilike(f"%{fabricante}%"))
    
    vacinas = query.offset(skip).limit(limit).all()
    return vacinas


@router.get("/vacinas/{vacina_id}", response_model=vacina_schemas.Vacina)
async def ler_vacina(
    vacina_id: str,
    db: Session = Depends(deps.get_db)
):
    """
    Obtém uma vacina pelo ID.
    """
    vacina = db.query(Vacina).filter(Vacina.vacina_id == vacina_id).first()
    if not vacina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacina não encontrada"
        )
    return vacina


@router.post("/vacinas/", response_model=vacina_schemas.Vacina, status_code=status.HTTP_201_CREATED)
async def criar_vacina(
    vacina_in: vacina_schemas.VacinaCreate,
    db: Session = Depends(deps.get_db)
):
    """
    Cria uma nova vacina.
    """
    nova_vacina = Vacina(
        nome=vacina_in.nome,
        fabricante=vacina_in.fabricante,
        lote=vacina_in.lote,
        validade=vacina_in.validade
    )
    
    db.add(nova_vacina)
    db.commit()
    db.refresh(nova_vacina)
    
    return nova_vacina


@router.put("/vacinas/{vacina_id}", response_model=vacina_schemas.Vacina)
async def atualizar_vacina(
    vacina_id: str,
    vacina_in: vacina_schemas.VacinaUpdate,
    db: Session = Depends(deps.get_db)
):
    """
    Atualiza uma vacina.
    """
    vacina = db.query(Vacina).filter(Vacina.vacina_id == vacina_id).first()
    if not vacina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacina não encontrada"
        )
    
    # Atualizar campos
    update_data = vacina_in.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(vacina, key, value)
    
    db.add(vacina)
    db.commit()
    db.refresh(vacina)
    
    return vacina


@router.delete("/vacinas/{vacina_id}", status_code=status.HTTP_204_NO_CONTENT)
async def remover_vacina(
    vacina_id: str,
    db: Session = Depends(deps.get_db)
):
    """
    Remove uma vacina.
    """
    vacina = db.query(Vacina).filter(Vacina.vacina_id == vacina_id).first()
    if not vacina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacina não encontrada"
        )
    
    # Verificar se a vacina está sendo usada na carteira de vacinação
    vacinacao = db.query(CarteiraVacinacao).filter(CarteiraVacinacao.vacina_id == vacina_id).first()
    if vacinacao:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Não é possível remover esta vacina pois ela está sendo utilizada em registros de vacinação"
        )
    
    db.delete(vacina)
    db.commit()
    
    return None


# ENDPOINTS PARA CARTEIRA DE VACINAÇÃO

@router.get("/carteira/", response_model=List[vacinacao_schemas.CarteiraVacinacaoCompleta])
async def listar_vacinacoes(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    paciente_id: Optional[str] = Query(None, description="Filtrar por ID do paciente")
):
    """
    Retorna os registros de vacinação.
    Opcionalmente filtra por paciente.
    """
    query = db.query(
        CarteiraVacinacao,
        Paciente.nome.label("nome_paciente"),
        Vacina.nome.label("nome_vacina"),
        Estabelecimento.nome.label("nome_estabelecimento"),
        Estabelecimento.tipo.label("tipo_estabelecimento"),
        Funcionario.nome.label("nome_funcionario")
    ).join(
        Paciente, CarteiraVacinacao.paciente_id == Paciente.paciente_id
    ).join(
        Vacina, CarteiraVacinacao.vacina_id == Vacina.vacina_id
    ).join(
        Estabelecimento, CarteiraVacinacao.estabelecimento_id == Estabelecimento.estabelecimento_id
    ).join(
        Funcionario, CarteiraVacinacao.funcionario_id == Funcionario.funcionario_id
    )
    
    if paciente_id:
        query = query.filter(CarteiraVacinacao.paciente_id == paciente_id)
    
    result = query.offset(skip).limit(limit).all()
    
    # Transformar resultados em objetos CarteiraVacinacaoCompleta
    vacinacoes = []
    for row in result:
        vacinacao = row[0]  # CarteiraVacinacao
        vacinacao_completa = vacinacao_schemas.CarteiraVacinacaoCompleta(
            **vacinacao.__dict__,
            nome_paciente=row.nome_paciente,
            nome_vacina=row.nome_vacina,
            nome_estabelecimento=row.nome_estabelecimento,
            tipo_estabelecimento=row.tipo_estabelecimento,
            nome_funcionario=row.nome_funcionario
        )
        vacinacoes.append(vacinacao_completa)
    
    return vacinacoes


@router.get("/carteira/paciente/{paciente_id}", response_model=vacinacao_schemas.CarteiraVacinacaoPaciente)
async def ler_carteira_paciente(
    paciente_id: str,
    db: Session = Depends(deps.get_db)
):
    """
    Obtém a carteira de vacinação completa de um paciente.
    """
    # Verificar se o paciente existe
    paciente = db.query(Paciente).filter(Paciente.paciente_id == paciente_id).first()
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    # Buscar todas as vacinas do paciente
    query = db.query(
        CarteiraVacinacao,
        Paciente.nome.label("nome_paciente"),
        Vacina.nome.label("nome_vacina"),
        Estabelecimento.nome.label("nome_estabelecimento"),
        Estabelecimento.tipo.label("tipo_estabelecimento"),
        Funcionario.nome.label("nome_funcionario")
    ).join(
        Paciente, CarteiraVacinacao.paciente_id == Paciente.paciente_id
    ).join(
        Vacina, CarteiraVacinacao.vacina_id == Vacina.vacina_id
    ).join(
        Estabelecimento, CarteiraVacinacao.estabelecimento_id == Estabelecimento.estabelecimento_id
    ).join(
        Funcionario, CarteiraVacinacao.funcionario_id == Funcionario.funcionario_id
    ).filter(
        CarteiraVacinacao.paciente_id == paciente_id
    ).order_by(
        CarteiraVacinacao.data_aplicacao.desc()
    )
    
    result = query.all()
    
    # Transformar resultados em objetos CarteiraVacinacaoCompleta
    vacinacoes = []
    for row in result:
        vacinacao = row[0]  # CarteiraVacinacao
        vacinacao_completa = vacinacao_schemas.CarteiraVacinacaoCompleta(
            **vacinacao.__dict__,
            nome_paciente=row.nome_paciente,
            nome_vacina=row.nome_vacina,
            nome_estabelecimento=row.nome_estabelecimento,
            tipo_estabelecimento=row.tipo_estabelecimento,
            nome_funcionario=row.nome_funcionario
        )
        vacinacoes.append(vacinacao_completa)
    
    # Retornar paciente e suas vacinações
    return vacinacao_schemas.CarteiraVacinacaoPaciente(
        paciente=paciente,
        vacinacoes=vacinacoes
    )


@router.post("/carteira/", response_model=vacinacao_schemas.CarteiraVacinacao, status_code=status.HTTP_201_CREATED)
async def registrar_vacinacao(
    vacinacao_in: vacinacao_schemas.CarteiraVacinacaoCreate,
    db: Session = Depends(deps.get_db)
):
    """
    Registra uma nova aplicação de vacina na carteira de vacinação.
    """
    # Verificar se o paciente existe
    paciente = db.query(Paciente).filter(Paciente.paciente_id == vacinacao_in.paciente_id).first()
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    
    # Verificar se a vacina existe
    vacina = db.query(Vacina).filter(Vacina.vacina_id == vacinacao_in.vacina_id).first()
    if not vacina:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Vacina não encontrada"
        )
    
    # Verificar se o funcionário existe
    funcionario = db.query(Funcionario).filter(Funcionario.funcionario_id == vacinacao_in.funcionario_id).first()
    if not funcionario:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Funcionário não encontrado"
        )
    
    # Verificar se o estabelecimento existe
    estabelecimento = db.query(Estabelecimento).filter(Estabelecimento.estabelecimento_id == vacinacao_in.estabelecimento_id).first()
    if not estabelecimento:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Estabelecimento não encontrado"
        )
    
    # Verificar se já existe um registro igual (mesma vacina, mesma dose e mesmo paciente)
    vacinacao_existente = db.query(CarteiraVacinacao).filter(
        and_(
            CarteiraVacinacao.paciente_id == vacinacao_in.paciente_id,
            CarteiraVacinacao.vacina_id == vacinacao_in.vacina_id,
            CarteiraVacinacao.dose == vacinacao_in.dose
        )
    ).first()
    
    if vacinacao_existente:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Paciente já recebeu esta dose ({vacinacao_in.dose}) desta vacina"
        )
    
    # Criar novo registro de vacinação
    nova_vacinacao = CarteiraVacinacao(
        paciente_id=vacinacao_in.paciente_id,
        vacina_id=vacinacao_in.vacina_id,
        funcionario_id=vacinacao_in.funcionario_id,
        estabelecimento_id=vacinacao_in.estabelecimento_id,
        data_aplicacao=vacinacao_in.data_aplicacao,
        dose=vacinacao_in.dose,
        observacoes=vacinacao_in.observacoes
    )
    
    db.add(nova_vacinacao)
    db.commit()
    db.refresh(nova_vacinacao)
    
    return nova_vacinacao 