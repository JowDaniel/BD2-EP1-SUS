#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Dependências para os endpoints da API
"""

from typing import Generator, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.core.config import settings

# Esquema de autenticação OAuth2 com password
oauth2_scheme = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/login/access-token")


# Função placeholder para autenticação de usuário
# Na implementação real, você validaria o token JWT e retornaria o usuário
def get_current_user():
    """
    Placeholder para obter o usuário atual.
    Na implementação real, validaria o token JWT e retornaria o usuário.
    """
    # Este é um placeholder - na implementação real você validaria o token
    # e retornaria o usuário correspondente
    return {"id": "placeholder", "is_active": True, "is_superuser": False}


def get_current_active_user(current_user = Depends(get_current_user)):
    """
    Verifica se o usuário atual está ativo.
    """
    if not current_user.get("is_active", False):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Usuário inativo",
        )
    return current_user 