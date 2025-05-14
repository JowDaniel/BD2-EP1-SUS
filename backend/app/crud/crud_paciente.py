#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CRUD para operações com Pacientes
"""

from typing import Any, Dict, List, Optional, Union
from uuid import UUID

from sqlalchemy.orm import Session

from app.db.models.paciente import Paciente
from app.schemas.paciente import PacienteCreate, PacienteUpdate


class CRUDPaciente:
    """
    Implementação de operações CRUD para Paciente
    """

    def get(self, db: Session, id: UUID) -> Optional[Paciente]:
        """
        Obtém um paciente por ID
        """
        return db.query(Paciente).filter(Paciente.paciente_id == id).first()

    def get_by_cpf(self, db: Session, cpf: str) -> Optional[Paciente]:
        """
        Obtém um paciente por CPF
        """
        return db.query(Paciente).filter(Paciente.cpf == cpf).first()

    def get_by_sus_numero(self, db: Session, sus_numero: str) -> Optional[Paciente]:
        """
        Obtém um paciente por número do SUS
        """
        return db.query(Paciente).filter(Paciente.sus_numero == sus_numero).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[Paciente]:
        """
        Obtém múltiplos pacientes com paginação
        """
        return db.query(Paciente).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: PacienteCreate) -> Paciente:
        """
        Cria um novo paciente
        """
        db_obj = Paciente(
            nome=obj_in.nome,
            cpf=obj_in.cpf,
            data_nascimento=obj_in.data_nascimento,
            sexo=obj_in.sexo,
            endereco=obj_in.endereco,
            telefone=obj_in.telefone,
            email=obj_in.email,
            tipo_sanguineo=obj_in.tipo_sanguineo,
            sus_numero=obj_in.sus_numero,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: Paciente,
        obj_in: Union[PacienteUpdate, Dict[str, Any]]
    ) -> Paciente:
        """
        Atualiza um paciente existente
        """
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        for field in update_data:
            if update_data[field] is not None:
                setattr(db_obj, field, update_data[field])
        
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: UUID) -> Paciente:
        """
        Remove um paciente
        """
        obj = db.query(Paciente).get(id)
        db.delete(obj)
        db.commit()
        return obj


# Instância do CRUD para importação de outros módulos
paciente = CRUDPaciente() 