-- Schema para o Sistema de Compartilhamento de Dados de Pacientes do SUS
-- SGBD: PostgreSQL

-- Extensão para UUID (identificadores únicos universais)
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";

-- Tabela de Pacientes
CREATE TABLE pacientes (
    paciente_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    data_nascimento DATE NOT NULL,
    sexo CHAR(1) CHECK (sexo IN ('M', 'F', 'O')),
    endereco VARCHAR(200),
    telefone VARCHAR(20),
    email VARCHAR(100),
    tipo_sanguineo VARCHAR(3),
    sus_numero VARCHAR(20) UNIQUE NOT NULL,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Estabelecimentos de Saúde (agrupa postos e hospitais)
CREATE TABLE estabelecimentos (
    estabelecimento_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(100) NOT NULL,
    tipo VARCHAR(50) NOT NULL CHECK (tipo IN ('POSTO', 'HOSPITAL', 'UPA', 'OUTRO')),
    cnes VARCHAR(20) UNIQUE NOT NULL, -- Cadastro Nacional de Estabelecimentos de Saúde
    endereco VARCHAR(200) NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    horario_funcionamento VARCHAR(100),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Funcionários
CREATE TABLE funcionarios (
    funcionario_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    estabelecimento_id UUID NOT NULL REFERENCES estabelecimentos(estabelecimento_id),
    nome VARCHAR(100) NOT NULL,
    cpf VARCHAR(14) UNIQUE NOT NULL,
    cargo VARCHAR(50) NOT NULL,
    registro_profissional VARCHAR(20), -- CRM, COREN, etc.
    data_contratacao DATE NOT NULL,
    telefone VARCHAR(20),
    email VARCHAR(100),
    ativo BOOLEAN DEFAULT TRUE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Prontuários
CREATE TABLE prontuarios (
    prontuario_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    paciente_id UUID NOT NULL REFERENCES pacientes(paciente_id),
    estabelecimento_id UUID NOT NULL REFERENCES estabelecimentos(estabelecimento_id),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    ultima_atualizacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Atendimentos
CREATE TABLE atendimentos (
    atendimento_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prontuario_id UUID NOT NULL REFERENCES prontuarios(prontuario_id),
    funcionario_id UUID NOT NULL REFERENCES funcionarios(funcionario_id),
    data_atendimento TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_atendimento VARCHAR(50) NOT NULL,
    descricao TEXT,
    diagnostico TEXT,
    observacoes TEXT
);

-- Tabela de Vacinas
CREATE TABLE vacinas (
    vacina_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(100) NOT NULL,
    fabricante VARCHAR(100),
    lote VARCHAR(50),
    validade DATE,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Carteira de Vacinação
CREATE TABLE carteira_vacinacao (
    vacinacao_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    paciente_id UUID NOT NULL REFERENCES pacientes(paciente_id),
    vacina_id UUID NOT NULL REFERENCES vacinas(vacina_id),
    funcionario_id UUID NOT NULL REFERENCES funcionarios(funcionario_id),
    estabelecimento_id UUID NOT NULL REFERENCES estabelecimentos(estabelecimento_id),
    data_aplicacao TIMESTAMP NOT NULL,
    dose VARCHAR(20) NOT NULL,
    observacoes TEXT,
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Medicamentos
CREATE TABLE medicamentos (
    medicamento_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    nome VARCHAR(100) NOT NULL,
    principio_ativo VARCHAR(100) NOT NULL,
    fabricante VARCHAR(100),
    data_cadastro TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Prescrições
CREATE TABLE prescricoes (
    prescricao_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    atendimento_id UUID NOT NULL REFERENCES atendimentos(atendimento_id),
    medicamento_id UUID NOT NULL REFERENCES medicamentos(medicamento_id),
    dosagem VARCHAR(50) NOT NULL,
    frequencia VARCHAR(50) NOT NULL,
    duracao VARCHAR(50),
    observacoes TEXT,
    data_prescricao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Tabela de Exames
CREATE TABLE exames (
    exame_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    atendimento_id UUID NOT NULL REFERENCES atendimentos(atendimento_id),
    tipo_exame VARCHAR(100) NOT NULL,
    resultado TEXT,
    data_solicitacao TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    data_realizacao TIMESTAMP,
    funcionario_solicitante UUID NOT NULL REFERENCES funcionarios(funcionario_id),
    funcionario_realizador UUID REFERENCES funcionarios(funcionario_id),
    observacoes TEXT
);

-- Tabela de Histórico de Acesso aos Prontuários
CREATE TABLE historico_acesso (
    acesso_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prontuario_id UUID NOT NULL REFERENCES prontuarios(prontuario_id),
    funcionario_id UUID NOT NULL REFERENCES funcionarios(funcionario_id),
    data_acesso TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
    tipo_acesso VARCHAR(50) NOT NULL,
    ip_acesso VARCHAR(50),
    observacoes TEXT
);

-- Índices para melhorar performance das consultas

-- Índice para busca de pacientes por CPF
CREATE INDEX idx_pacientes_cpf ON pacientes(cpf);

-- Índice para busca de pacientes por número do SUS
CREATE INDEX idx_pacientes_sus ON pacientes(sus_numero);

-- Índice para busca de funcionários por registro profissional
CREATE INDEX idx_funcionarios_registro ON funcionarios(registro_profissional);

-- Índice para busca rápida de atendimentos por data
CREATE INDEX idx_atendimentos_data ON atendimentos(data_atendimento);

-- Índice para busca rápida de vacinações por paciente
CREATE INDEX idx_vacinacao_paciente ON carteira_vacinacao(paciente_id);

-- Índice para busca rápida de prontuários por paciente
CREATE INDEX idx_prontuarios_paciente ON prontuarios(paciente_id);

-- Índice para busca rápida de atendimentos por prontuário
CREATE INDEX idx_atendimentos_prontuario ON atendimentos(prontuario_id);

-- Comentários nas tabelas
COMMENT ON TABLE pacientes IS 'Armazena informações dos pacientes do SUS';
COMMENT ON TABLE estabelecimentos IS 'Armazena informações dos postos de saúde e hospitais';
COMMENT ON TABLE funcionarios IS 'Armazena informações dos profissionais de saúde';
COMMENT ON TABLE prontuarios IS 'Registro central de prontuários dos pacientes';
COMMENT ON TABLE atendimentos IS 'Registros de atendimentos médicos';
COMMENT ON TABLE vacinas IS 'Cadastro de vacinas disponíveis';
COMMENT ON TABLE carteira_vacinacao IS 'Registros de vacinação dos pacientes';
COMMENT ON TABLE medicamentos IS 'Cadastro de medicamentos';
COMMENT ON TABLE prescricoes IS 'Prescrições médicas geradas nos atendimentos';
COMMENT ON TABLE exames IS 'Registros de exames solicitados e realizados';
COMMENT ON TABLE historico_acesso IS 'Log de acesso aos prontuários para auditoria'; 