# Frontend do Sistema de Compartilhamento de Dados de Pacientes do SUS

## Tecnologias Utilizadas

- **React 18**: Biblioteca JavaScript para construção de interfaces
- **Material-UI**: Framework de design para componentes React
- **React Router**: Roteamento para aplicações React
- **Axios**: Cliente HTTP para comunicação com o backend

## Estrutura do Projeto

```
frontend/
├── public/               # Arquivos públicos estáticos
│   └── index.html        # Template HTML principal
├── src/                  # Código fonte da aplicação
│   ├── components/       # Componentes reutilizáveis
│   ├── pages/            # Páginas da aplicação
│   ├── services/         # Serviços para comunicação com a API
│   ├── context/          # Contextos React (estado global)
│   ├── utils/            # Utilitários e funções auxiliares
│   ├── App.js            # Componente principal da aplicação
│   └── index.js          # Ponto de entrada da aplicação
└── package.json          # Configuração do projeto e dependências
```

## Instalação e Execução

### Com Docker (recomendado)

1. Certifique-se de ter o Docker e o Docker Compose instalados
2. Na raiz do projeto, execute:
   ```
   docker-compose up -d
   ```
3. O frontend estará disponível em `http://localhost:3000`

### Sem Docker

1. Certifique-se de ter o Node.js 18+ instalado
2. Instale as dependências:
   ```
   npm install
   ```
3. Execute a aplicação:
   ```
   npm start
   ```
4. O frontend estará disponível em `http://localhost:3000`

## Desenvolvimento

### Componentes e Páginas

- `components/`: Contém componentes reutilizáveis (botões, campos, tabelas, etc.)
- `pages/`: Contém páginas completas da aplicação

### Comunicação com o Backend

- `services/api.js`: Configuração do cliente Axios
- `services/pacientes.js`: Funções para acessar endpoints de pacientes
- `services/prontuarios.js`: Funções para acessar endpoints de prontuários
- `services/vacinacao.js`: Funções para acessar endpoints de vacinação

### Build para Produção

```
npm run build
```

Este comando gera uma versão otimizada do aplicativo para produção na pasta `build/`.

### Testes

```
npm test
```

Execute os testes unitários e de integração. 