# 🩺 Sistema de Compartilhamento de Dados de Pacientes do SUS

## Descrição Geral
Sistema para centralizar e compartilhar dados de pacientes (carteirinhas de vacinação e prontuários médicos) entre postos de saúde e hospitais do SUS. O sistema assegura segurança, acessibilidade e eficiência no gerenciamento das informações, com foco em consultas otimizadas e modelagem de dados eficiente.

## Tecnologias

- **Banco de Dados:** PostgreSQL
- **Backend:** Python com FastAPI
- **Frontend:** React com Material-UI
- **Deployment:** Docker e Docker Compose

## Funcionalidades Principais

- Cadastro e gerenciamento de pacientes
- Consulta de estabelecimentos de saúde (Hospitais, UBS, UPA)
- Gerenciamento de vacinas e carteiras de vacinação
- Prontuários médicos compartilhados entre estabelecimentos

## Pré-requisitos

- Docker
- Docker Compose
- Git

## Como clonar e executar o projeto

### 1. Clone o repositório

```bash
# Clone o repositório
git clone https://github.com/JowDaniel/BD2-EP1-SUS.git

# Entre no diretório do projeto
cd BD2-EP1-SUS
```

### 2. Executando o Sistema

Você pode executar o sistema completo de duas maneiras:

#### Usando o script de inicialização

```bash
# Dar permissão de execução ao script (necessário apenas na primeira vez)
chmod +x start.sh

# Executar o script
./start.sh
```

#### Manualmente com Docker Compose

```bash
# Parar qualquer instância anterior
docker compose down

# Remover volumes antigos (opcional)
docker volume rm ep1_postgres_data

# Reconstruir as imagens (se necessário)
docker compose build

# Iniciar o sistema
docker compose up
```

## Acessando o Sistema

Após a inicialização, o sistema estará disponível nos seguintes endereços:

- **Frontend:** http://localhost:3000
- **API Backend:** http://localhost:8000
- **Documentação da API:** http://localhost:8000/docs

## Estrutura do Projeto
```
/
├── docs/                       # Documentação
│   ├── diagrama-er.png         # Diagrama Entidade-Relacionamento
│   └── modelo-logico.png       # Modelo Lógico
├── sql/                        # Scripts SQL
│   ├── ddl/                    # Criação de tabelas e estruturas
│   ├── dml/                    # Inserção de dados de teste
│   └── queries/                # Consultas otimizadas
├── backend/                    # API Python FastAPI
│   ├── app/                    # Código da aplicação
│   │   ├── api/                # Endpoints da API
│   │   ├── core/               # Configurações centrais
│   │   ├── db/                 # Modelos e conexão com banco
│   │   ├── schemas/            # Schemas Pydantic
│   │   └── services/           # Lógica de negócio
│   ├── requirements.txt        # Dependências Python
│   └── main.py                 # Ponto de entrada da aplicação
├── frontend/                   # Aplicação React
└── docker/                     # Configurações Docker
```

## Entidades Principais
- Pacientes
- Carteirinhas de Vacinação
- Prontuários Médicos
- Postos de Saúde
- Hospitais
- Funcionários

## Próximos Passos
1. Modelagem da Base de Dados (Diagrama ER e Modelo Lógico)
2. Implementação do Schema SQL (DDL)
3. Inserção de dados de teste (DML)
4. Implementação das consultas críticas com otimização
5. Desenvolvimento do aplicativo funcional 

## Resolução de Problemas

Se encontrar algum problema ao executar o sistema, tente os seguintes passos:

1. **Problemas com o banco de dados**:
   ```bash
   docker compose down
   docker volume rm ep1_postgres_data
   docker compose up
   ```

2. **Problemas com as dependências**:
   ```bash
   docker compose build --no-cache
   docker compose up
   ```

3. **Ver logs de um serviço específico**:
   ```bash
   docker compose logs [serviço]
   ```
   Onde [serviço] pode ser: postgres, backend ou frontend

## Desenvolvimento

Para desenvolver novas funcionalidades:

1. Faça as alterações nos arquivos correspondentes
2. Reconstrua a imagem Docker afetada: `docker compose build [serviço]`
3. Reinicie os serviços: `docker compose up`

O código-fonte está montado como volumes nos containers, então muitas alterações são refletidas automaticamente sem necessidade de reconstruir as imagens.

## Contribuição

Para contribuir com o projeto:

1. Crie um fork do repositório
2. Crie uma branch para sua feature (`git checkout -b feature/nova-funcionalidade`)
3. Faça commit das suas alterações (`git commit -am 'Adiciona nova funcionalidade'`)
4. Faça push para a branch (`git push origin feature/nova-funcionalidade`)
5. Crie um novo Pull Request 