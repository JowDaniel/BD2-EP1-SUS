# Backend do Sistema de Compartilhamento de Dados de Pacientes do SUS

## Tecnologias Utilizadas

- **Python 3.11**: Linguagem de programação moderna e expressiva
- **FastAPI**: Framework web de alta performance para APIs
- **SQLAlchemy**: ORM para interação com o banco de dados
- **Pydantic**: Validação de dados e serialização
- **PostgreSQL**: Banco de dados relacional robusto
- **JWT**: Autenticação baseada em tokens

## Estrutura do Projeto

```
backend/
├── app/                  # Código da aplicação
│   ├── api/              # Endpoints da API
│   │   ├── endpoints/    # Endpoints específicos por recurso
│   │   └── deps.py       # Dependências da API (autenticação, banco)
│   ├── core/             # Configurações centrais
│   │   └── config.py     # Configurações da aplicação
│   ├── db/               # Modelos e conexão com banco
│   │   ├── models/       # Modelos SQLAlchemy
│   │   └── session.py    # Sessão do banco de dados
│   ├── schemas/          # Schemas Pydantic para validação
│   └── services/         # Lógica de negócio
├── requirements.txt      # Dependências Python
└── main.py               # Ponto de entrada da aplicação
```

## Instalação e Execução

### Com Docker (recomendado)

1. Certifique-se de ter o Docker e o Docker Compose instalados
2. Na raiz do projeto, execute:
   ```
   docker-compose up -d
   ```
3. O backend estará disponível em `http://localhost:8000`
4. Acesse a documentação da API em `http://localhost:8000/docs`

### Sem Docker

1. Certifique-se de ter o Python 3.11+ instalado
2. Crie um ambiente virtual:
   ```
   python -m venv venv
   source venv/bin/activate  # Linux/Mac
   venv\Scripts\activate     # Windows
   ```
3. Instale as dependências:
   ```
   pip install -r requirements.txt
   ```
4. Configure as variáveis de ambiente (ou crie um arquivo `.env`)
5. Execute a aplicação:
   ```
   uvicorn main:app --reload
   ```

## Desenvolvimento

- Use `black` para formatação do código
- Use `isort` para organizar os imports
- Use `flake8` para verificar erros e estilo de código
- Execute os testes com `pytest` 