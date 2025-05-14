#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Configuração do roteador principal da API
"""

from fastapi import APIRouter

from app.api.endpoints import pacientes, prontuarios, estabelecimentos, vacinacao, funcionarios, autenticacao

# Roteador principal que agrupa todos os endpoints da API
api_router = APIRouter()

# Inclusão dos roteadores específicos por entidade/funcionalidade
api_router.include_router(autenticacao.router, tags=["autenticação"])
api_router.include_router(pacientes.router, prefix="/pacientes", tags=["pacientes"])
api_router.include_router(prontuarios.router, prefix="/prontuarios", tags=["prontuários"])
api_router.include_router(estabelecimentos.router, prefix="/estabelecimentos", tags=["estabelecimentos"])
api_router.include_router(vacinacao.router, prefix="/vacinacao", tags=["vacinação"])
api_router.include_router(funcionarios.router, prefix="/funcionarios", tags=["funcionários"]) 