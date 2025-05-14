#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Endpoints para autenticação
"""

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

router = APIRouter()


@router.post("/login/access-token")
async def login_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    """
    Endpoint simples para autenticação OAuth2 (placeholder)
    """
    # Em uma implementação real, verificaríamos as credenciais no banco de dados
    # e retornaríamos um token JWT
    if form_data.username == "admin" and form_data.password == "admin":
        return {
            "access_token": "placeholder_token",
            "token_type": "bearer",
        }
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    ) 