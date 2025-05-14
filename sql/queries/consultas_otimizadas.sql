-- Consultas Otimizadas para o Sistema de Compartilhamento de Dados de Pacientes do SUS
-- SGBD: PostgreSQL

----------------------------------------------
-- CONSULTA 1: Listar todos os pacientes com suas informações básicas
-- Otimização: Índice em CPF e Número SUS já criados
----------------------------------------------

EXPLAIN ANALYZE
SELECT 
    p.nome, 
    p.cpf, 
    p.data_nascimento, 
    p.sus_numero, 
    p.tipo_sanguineo
FROM 
    pacientes p
ORDER BY 
    p.nome;

----------------------------------------------
-- CONSULTA 2: Buscar histórico de atendimentos de um paciente específico
-- Otimização: Utilização de índices em relacionamentos e JOIN otimizado
----------------------------------------------

EXPLAIN ANALYZE
SELECT 
    p.nome AS paciente, 
    e.nome AS estabelecimento,
    a.data_atendimento, 
    a.tipo_atendimento, 
    a.diagnostico,
    f.nome AS profissional,
    f.registro_profissional
FROM 
    atendimentos a
JOIN 
    prontuarios pr ON a.prontuario_id = pr.prontuario_id
JOIN 
    pacientes p ON pr.paciente_id = p.paciente_id
JOIN 
    funcionarios f ON a.funcionario_id = f.funcionario_id
JOIN 
    estabelecimentos e ON pr.estabelecimento_id = e.estabelecimento_id
WHERE 
    p.cpf = '123.456.789-00'  -- Parâmetro: CPF do paciente
ORDER BY 
    a.data_atendimento DESC;

----------------------------------------------
-- CONSULTA 3: Carteira de vacinação completa de um paciente
-- Otimização: Uso de índices e JOINs otimizados
----------------------------------------------

EXPLAIN ANALYZE
SELECT 
    p.nome AS paciente, 
    p.sus_numero,
    v.nome AS vacina,
    v.fabricante,
    cv.dose,
    cv.data_aplicacao,
    e.nome AS local_aplicacao,
    f.nome AS profissional_aplicador
FROM 
    carteira_vacinacao cv
JOIN 
    pacientes p ON cv.paciente_id = p.paciente_id
JOIN 
    vacinas v ON cv.vacina_id = v.vacina_id
JOIN 
    funcionarios f ON cv.funcionario_id = f.funcionario_id
JOIN 
    estabelecimentos e ON cv.estabelecimento_id = e.estabelecimento_id
WHERE 
    p.sus_numero = '789123456789012'  -- Parâmetro: Número SUS do paciente
ORDER BY 
    v.nome, cv.data_aplicacao;

----------------------------------------------
-- CONSULTA 4: Listar todos os estabelecimentos com contagem de atendimentos nos últimos 30 dias
-- Otimização: Uso de índice em data_atendimento e agregação
----------------------------------------------

EXPLAIN ANALYZE
SELECT 
    e.nome AS estabelecimento,
    e.tipo,
    e.endereco,
    COUNT(a.atendimento_id) AS total_atendimentos_recentes
FROM 
    estabelecimentos e
LEFT JOIN 
    prontuarios pr ON e.estabelecimento_id = pr.estabelecimento_id
LEFT JOIN 
    atendimentos a ON pr.prontuario_id = a.prontuario_id AND a.data_atendimento >= CURRENT_DATE - INTERVAL '30 days'
GROUP BY 
    e.estabelecimento_id
ORDER BY 
    total_atendimentos_recentes DESC;

----------------------------------------------
-- CONSULTA 5: Relatório de pacientes por tipo sanguíneo (para campanhas de doação)
-- Otimização: Agregação e ordenação
----------------------------------------------

EXPLAIN ANALYZE
SELECT 
    tipo_sanguineo,
    COUNT(*) AS total_pacientes
FROM 
    pacientes
WHERE 
    tipo_sanguineo IS NOT NULL
GROUP BY 
    tipo_sanguineo
ORDER BY 
    total_pacientes DESC;

----------------------------------------------
-- CONSULTA 6: Buscar medicamentos prescritos para um paciente específico
-- Otimização: Múltiplos JOINs otimizados e uso de índices
----------------------------------------------

EXPLAIN ANALYZE
SELECT 
    p.nome AS paciente,
    a.data_atendimento,
    m.nome AS medicamento,
    m.principio_ativo,
    pr.dosagem,
    pr.frequencia,
    pr.duracao,
    f.nome AS medico_prescritor,
    f.registro_profissional
FROM 
    prescricoes pr
JOIN 
    atendimentos a ON pr.atendimento_id = a.atendimento_id
JOIN 
    prontuarios pron ON a.prontuario_id = pron.prontuario_id
JOIN 
    pacientes p ON pron.paciente_id = p.paciente_id
JOIN 
    medicamentos m ON pr.medicamento_id = m.medicamento_id
JOIN 
    funcionarios f ON a.funcionario_id = f.funcionario_id
WHERE 
    p.cpf = '987.654.321-00'  -- Parâmetro: CPF do paciente
ORDER BY 
    a.data_atendimento DESC;

----------------------------------------------
-- CONSULTA 7: Relatório de vacinas aplicadas por mês
-- Otimização: Uso de funções de data e agregação
----------------------------------------------

EXPLAIN ANALYZE
SELECT 
    TO_CHAR(cv.data_aplicacao, 'YYYY-MM') AS mes_ano,
    v.nome AS vacina,
    COUNT(*) AS total_aplicacoes
FROM 
    carteira_vacinacao cv
JOIN 
    vacinas v ON cv.vacina_id = v.vacina_id
WHERE 
    cv.data_aplicacao >= CURRENT_DATE - INTERVAL '1 year'
GROUP BY 
    mes_ano, v.nome
ORDER BY 
    mes_ano DESC, total_aplicacoes DESC;

----------------------------------------------
-- CONSULTA 8: Identificar profissionais de saúde que mais realizaram atendimentos
-- Otimização: Agregação e índice em funcionario_id
----------------------------------------------

EXPLAIN ANALYZE
SELECT 
    f.nome AS profissional,
    f.registro_profissional,
    f.cargo,
    e.nome AS estabelecimento,
    COUNT(a.atendimento_id) AS total_atendimentos
FROM 
    funcionarios f
JOIN 
    estabelecimentos e ON f.estabelecimento_id = e.estabelecimento_id
LEFT JOIN 
    atendimentos a ON f.funcionario_id = a.funcionario_id
GROUP BY 
    f.funcionario_id, e.nome
ORDER BY 
    total_atendimentos DESC;

----------------------------------------------
-- CONSULTA 9: Buscar histórico de acesso aos prontuários (auditoria)
-- Otimização: Índices de tempo e filtro por período
----------------------------------------------

EXPLAIN ANALYZE
SELECT 
    ha.data_acesso,
    ha.tipo_acesso,
    ha.ip_acesso,
    p.nome AS paciente,
    p.sus_numero,
    f.nome AS funcionario,
    f.cargo,
    e.nome AS estabelecimento
FROM 
    historico_acesso ha
JOIN 
    prontuarios pr ON ha.prontuario_id = pr.prontuario_id
JOIN 
    pacientes p ON pr.paciente_id = p.paciente_id
JOIN 
    funcionarios f ON ha.funcionario_id = f.funcionario_id
JOIN 
    estabelecimentos e ON f.estabelecimento_id = e.estabelecimento_id
WHERE 
    ha.data_acesso BETWEEN CURRENT_DATE - INTERVAL '7 days' AND CURRENT_DATE
ORDER BY 
    ha.data_acesso DESC;

----------------------------------------------
-- CONSULTA 10: Estatísticas de diagnósticos mais frequentes
-- Otimização: Agregação e uso de function para normalizar diagnósticos
----------------------------------------------

EXPLAIN ANALYZE
SELECT 
    COALESCE(diagnostico, 'Não especificado') AS diagnostico,
    COUNT(*) AS total_casos
FROM 
    atendimentos
WHERE 
    data_atendimento >= CURRENT_DATE - INTERVAL '90 days'
GROUP BY 
    diagnostico
ORDER BY 
    total_casos DESC
LIMIT 10;

----------------------------------------------
-- VIEW MATERIALIZADA: Resumo dos prontuários
-- Otimização: Pré-processamento dos dados mais acessados
----------------------------------------------

-- Criação da view materializada
CREATE MATERIALIZED VIEW IF NOT EXISTS mv_resumo_prontuarios AS
SELECT 
    p.paciente_id,
    p.nome,
    p.cpf,
    p.sus_numero,
    p.data_nascimento,
    p.tipo_sanguineo,
    pr.prontuario_id,
    COUNT(DISTINCT a.atendimento_id) AS total_atendimentos,
    MAX(a.data_atendimento) AS ultimo_atendimento,
    COUNT(DISTINCT cv.vacinacao_id) AS total_vacinas,
    COUNT(DISTINCT ex.exame_id) AS total_exames
FROM 
    pacientes p
JOIN 
    prontuarios pr ON p.paciente_id = pr.paciente_id
LEFT JOIN 
    atendimentos a ON pr.prontuario_id = a.prontuario_id
LEFT JOIN 
    carteira_vacinacao cv ON p.paciente_id = cv.paciente_id
LEFT JOIN 
    exames ex ON a.atendimento_id = ex.atendimento_id
GROUP BY 
    p.paciente_id, p.nome, p.cpf, p.sus_numero, p.data_nascimento, p.tipo_sanguineo, pr.prontuario_id
WITH DATA;

-- Índice na view materializada
CREATE UNIQUE INDEX IF NOT EXISTS idx_mv_resumo_prontuarios_paciente_id ON mv_resumo_prontuarios(paciente_id);
CREATE INDEX IF NOT EXISTS idx_mv_resumo_prontuarios_cpf ON mv_resumo_prontuarios(cpf);
CREATE INDEX IF NOT EXISTS idx_mv_resumo_prontuarios_sus ON mv_resumo_prontuarios(sus_numero);

-- Consulta usando a view materializada
EXPLAIN ANALYZE
SELECT * FROM mv_resumo_prontuarios
WHERE cpf = '123.456.789-00';

----------------------------------------------
-- PARTICIONAMENTO: Exemplo de tabela particionada para histórico de atendimentos
-- Otimização: Particionamento por data para grandes volumes de dados históricos
----------------------------------------------

-- Criação de tabela particionada (exemplo conceitual)
/*
CREATE TABLE atendimentos_particionado (
    atendimento_id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    prontuario_id UUID NOT NULL,
    funcionario_id UUID NOT NULL,
    data_atendimento TIMESTAMP NOT NULL,
    tipo_atendimento VARCHAR(50) NOT NULL,
    descricao TEXT,
    diagnostico TEXT,
    observacoes TEXT
) PARTITION BY RANGE (data_atendimento);

-- Partições por trimestre (exemplo)
CREATE TABLE atendimentos_2023_q1 PARTITION OF atendimentos_particionado
    FOR VALUES FROM ('2023-01-01') TO ('2023-04-01');
    
CREATE TABLE atendimentos_2023_q2 PARTITION OF atendimentos_particionado
    FOR VALUES FROM ('2023-04-01') TO ('2023-07-01');
    
CREATE TABLE atendimentos_2023_q3 PARTITION OF atendimentos_particionado
    FOR VALUES FROM ('2023-07-01') TO ('2023-10-01');
    
CREATE TABLE atendimentos_2023_q4 PARTITION OF atendimentos_particionado
    FOR VALUES FROM ('2023-10-01') TO ('2024-01-01');
*/

----------------------------------------------
-- ÍNDICES ADICIONAIS: Estratégias para melhorar performance
----------------------------------------------

-- Índice composto para buscas frequentes por data + tipo de atendimento
CREATE INDEX IF NOT EXISTS idx_atendimentos_data_tipo ON atendimentos(data_atendimento, tipo_atendimento);

-- Índice para buscas por diagnóstico
CREATE INDEX IF NOT EXISTS idx_atendimentos_diagnostico ON atendimentos(diagnostico);

-- Índice para buscas de pacientes por nome (usando índice de texto para busca parcial)
CREATE INDEX IF NOT EXISTS idx_pacientes_nome ON pacientes(nome text_pattern_ops);

-- Índice para pesquisa de histórico por intervalo de datas
CREATE INDEX IF NOT EXISTS idx_historico_acesso_data ON historico_acesso(data_acesso);

-- Índice para prescrições por data
CREATE INDEX IF NOT EXISTS idx_prescricoes_data ON prescricoes(data_prescricao);

----------------------------------------------
-- FUNÇÃO: Obter prontuário completo de um paciente
-- Otimização: Função PL/pgSQL para simplificar a obtenção de dados complexos
----------------------------------------------

CREATE OR REPLACE FUNCTION obter_prontuario_completo(p_cpf VARCHAR)
RETURNS TABLE (
    paciente_nome VARCHAR,
    paciente_cpf VARCHAR,
    paciente_sus VARCHAR,
    paciente_nascimento DATE,
    paciente_tipo_sanguineo VARCHAR,
    atendimento_data TIMESTAMP,
    atendimento_tipo VARCHAR,
    atendimento_diagnostico TEXT,
    atendimento_medico VARCHAR,
    medicamento_nome VARCHAR,
    medicamento_dosagem VARCHAR,
    medicamento_frequencia VARCHAR,
    medicamento_duracao VARCHAR,
    exame_tipo VARCHAR,
    exame_data_solicitacao TIMESTAMP,
    exame_resultado TEXT,
    vacina_nome VARCHAR,
    vacina_data TIMESTAMP,
    vacina_dose VARCHAR
) AS $$
BEGIN
    RETURN QUERY
    WITH dados_paciente AS (
        SELECT 
            p.paciente_id, p.nome, p.cpf, p.sus_numero, p.data_nascimento, p.tipo_sanguineo
        FROM 
            pacientes p
        WHERE 
            p.cpf = p_cpf
    ),
    prontuarios_paciente AS (
        SELECT 
            pr.prontuario_id
        FROM 
            prontuarios pr
        JOIN 
            dados_paciente dp ON pr.paciente_id = dp.paciente_id
    ),
    atendimentos_paciente AS (
        SELECT 
            a.atendimento_id, a.data_atendimento, a.tipo_atendimento, a.diagnostico,
            f.nome AS medico_nome
        FROM 
            atendimentos a
        JOIN 
            prontuarios_paciente pp ON a.prontuario_id = pp.prontuario_id
        JOIN 
            funcionarios f ON a.funcionario_id = f.funcionario_id
    ),
    prescricoes_paciente AS (
        SELECT 
            ap.atendimento_id, m.nome AS medicamento_nome, 
            pr.dosagem, pr.frequencia, pr.duracao
        FROM 
            prescricoes pr
        JOIN 
            atendimentos_paciente ap ON pr.atendimento_id = ap.atendimento_id
        JOIN 
            medicamentos m ON pr.medicamento_id = m.medicamento_id
    ),
    exames_paciente AS (
        SELECT 
            ap.atendimento_id, e.tipo_exame, e.data_solicitacao, e.resultado
        FROM 
            exames e
        JOIN 
            atendimentos_paciente ap ON e.atendimento_id = ap.atendimento_id
    ),
    vacinas_paciente AS (
        SELECT 
            v.nome AS vacina_nome, cv.data_aplicacao, cv.dose
        FROM 
            carteira_vacinacao cv
        JOIN 
            dados_paciente dp ON cv.paciente_id = dp.paciente_id
        JOIN 
            vacinas v ON cv.vacina_id = v.vacina_id
    )
    SELECT 
        dp.nome, dp.cpf, dp.sus_numero, dp.data_nascimento, dp.tipo_sanguineo,
        ap.data_atendimento, ap.tipo_atendimento, ap.diagnostico, ap.medico_nome,
        pp.medicamento_nome, pp.dosagem, pp.frequencia, pp.duracao,
        ep.tipo_exame, ep.data_solicitacao, ep.resultado,
        vp.vacina_nome, vp.data_aplicacao, vp.dose
    FROM 
        dados_paciente dp
    LEFT JOIN 
        atendimentos_paciente ap ON TRUE
    LEFT JOIN 
        prescricoes_paciente pp ON ap.atendimento_id = pp.atendimento_id
    LEFT JOIN 
        exames_paciente ep ON ap.atendimento_id = ep.atendimento_id
    LEFT JOIN 
        vacinas_paciente vp ON TRUE
    ORDER BY 
        ap.data_atendimento DESC, vp.data_aplicacao DESC;
END;
$$ LANGUAGE plpgsql; 