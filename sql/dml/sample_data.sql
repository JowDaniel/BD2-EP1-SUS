-- Dados de exemplo para o Sistema de Compartilhamento de Dados de Pacientes do SUS
-- SGBD: PostgreSQL

-- Inserção de Pacientes
INSERT INTO pacientes (nome, cpf, data_nascimento, sexo, endereco, telefone, email, tipo_sanguineo, sus_numero)
VALUES
    ('Maria Silva', '123.456.789-00', '1980-05-15', 'F', 'Rua das Flores, 123, São Paulo, SP', '(11) 98765-4321', 'maria.silva@email.com', 'O+', '789123456789012'),
    ('João Santos', '987.654.321-00', '1975-10-20', 'M', 'Av. Paulista, 1000, São Paulo, SP', '(11) 91234-5678', 'joao.santos@email.com', 'A-', '456789123456789'),
    ('Ana Oliveira', '456.789.123-00', '1990-03-25', 'F', 'Rua Augusta, 500, São Paulo, SP', '(11) 95555-9999', 'ana.oliveira@email.com', 'B+', '123456789123456'),
    ('Carlos Pereira', '321.654.987-00', '1985-07-12', 'M', 'Rua Oscar Freire, 200, São Paulo, SP', '(11) 94444-8888', 'carlos.pereira@email.com', 'AB+', '987654321987654'),
    ('Fernanda Lima', '654.321.987-00', '1995-12-30', 'F', 'Rua Consolação, 300, São Paulo, SP', '(11) 93333-7777', 'fernanda.lima@email.com', 'O-', '321987654321987');

-- Inserção de Estabelecimentos
INSERT INTO estabelecimentos (nome, tipo, cnes, endereco, telefone, email, horario_funcionamento)
VALUES
    ('UBS Vila Mariana', 'POSTO', '1234567', 'Rua Domingos de Morais, 1200, Vila Mariana, São Paulo, SP', '(11) 5555-1234', 'ubs.vilamariana@saude.gov.br', 'Segunda a Sexta, 7h às 19h'),
    ('Hospital Municipal Vila Nova Cachoeirinha', 'HOSPITAL', '7654321', 'Av. Deputado Emílio Carlos, 3000, Limão, São Paulo, SP', '(11) 3986-1000', 'hmvnc@saude.gov.br', '24 horas, todos os dias'),
    ('UPA Jabaquara', 'UPA', '9876543', 'Rua das Rosas, 86, Jabaquara, São Paulo, SP', '(11) 5021-6500', 'upa.jabaquara@saude.gov.br', '24 horas, todos os dias'),
    ('Centro de Saúde Escola Barra Funda', 'POSTO', '5432198', 'Rua Dr. Abraão Ribeiro, 283, Barra Funda, São Paulo, SP', '(11) 3466-2500', 'csebf@saude.gov.br', 'Segunda a Sexta, 7h às 19h'),
    ('Hospital Estadual Mário Covas', 'HOSPITAL', '8765432', 'Rua Dr. Henrique Calderazzo, 321, Santo André, SP', '(11) 2829-5000', 'hemc@saude.gov.br', '24 horas, todos os dias');

-- Inserção de Funcionários
INSERT INTO funcionarios (estabelecimento_id, nome, cpf, cargo, registro_profissional, data_contratacao, telefone, email)
VALUES
    ((SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'UBS Vila Mariana'), 'Dr. Roberto Almeida', '111.222.333-44', 'Médico Clínico Geral', 'CRM-12345', '2018-03-10', '(11) 97777-8888', 'dr.roberto@saude.gov.br'),
    ((SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'UBS Vila Mariana'), 'Enfermeira Patrícia Souza', '222.333.444-55', 'Enfermeira', 'COREN-54321', '2019-06-15', '(11) 96666-7777', 'patricia.enfermeira@saude.gov.br'),
    ((SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'Hospital Municipal Vila Nova Cachoeirinha'), 'Dr. Marcos Pereira', '333.444.555-66', 'Médico Cardiologista', 'CRM-67890', '2015-01-20', '(11) 95555-6666', 'dr.marcos@saude.gov.br'),
    ((SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'Hospital Municipal Vila Nova Cachoeirinha'), 'Enfermeiro João Silva', '444.555.666-77', 'Enfermeiro', 'COREN-98765', '2017-09-05', '(11) 94444-5555', 'joao.enfermeiro@saude.gov.br'),
    ((SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'UPA Jabaquara'), 'Dra. Camila Oliveira', '555.666.777-88', 'Médica Emergencista', 'CRM-24680', '2020-02-18', '(11) 93333-4444', 'dra.camila@saude.gov.br');

-- Inserção de Prontuários
INSERT INTO prontuarios (paciente_id, estabelecimento_id)
VALUES
    ((SELECT paciente_id FROM pacientes WHERE cpf = '123.456.789-00'), (SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'UBS Vila Mariana')),
    ((SELECT paciente_id FROM pacientes WHERE cpf = '987.654.321-00'), (SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'Hospital Municipal Vila Nova Cachoeirinha')),
    ((SELECT paciente_id FROM pacientes WHERE cpf = '456.789.123-00'), (SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'UPA Jabaquara')),
    ((SELECT paciente_id FROM pacientes WHERE cpf = '321.654.987-00'), (SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'Centro de Saúde Escola Barra Funda')),
    ((SELECT paciente_id FROM pacientes WHERE cpf = '654.321.987-00'), (SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'Hospital Estadual Mário Covas'));

-- Inserção de Atendimentos
INSERT INTO atendimentos (prontuario_id, funcionario_id, data_atendimento, tipo_atendimento, descricao, diagnostico)
VALUES
    ((SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '123.456.789-00')), 
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '111.222.333-44'),
     '2023-05-10 09:30:00', 'Consulta Regular', 'Paciente relata dores de cabeça frequentes', 'Enxaqueca tensional'),
    
    ((SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '987.654.321-00')), 
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '333.444.555-66'),
     '2023-06-15 14:00:00', 'Cardiologia', 'Paciente com queixa de dor no peito', 'Angina estável'),
    
    ((SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '456.789.123-00')), 
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '555.666.777-88'),
     '2023-07-20 22:15:00', 'Emergência', 'Paciente com febre alta e dor abdominal', 'Infecção urinária'),
    
    ((SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '123.456.789-00')), 
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '111.222.333-44'),
     '2023-08-05 10:45:00', 'Retorno', 'Paciente retorna para avaliar tratamento de enxaqueca', 'Melhora do quadro de enxaqueca'),
    
    ((SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '987.654.321-00')), 
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '333.444.555-66'),
     '2023-09-10 15:30:00', 'Exame', 'Paciente realiza eletrocardiograma de rotina', 'Resultado normal, sem alterações');

-- Inserção de Vacinas
INSERT INTO vacinas (nome, fabricante, lote, validade)
VALUES
    ('Coronavac', 'Sinovac/Butantan', 'COVA123456', '2024-06-30'),
    ('Pfizer COVID-19', 'Pfizer/BioNTech', 'PFZ789012', '2024-08-15'),
    ('Tríplice Viral', 'Bio-Manguinhos', 'TRV456789', '2025-03-20'),
    ('Influenza', 'Butantan', 'INF234567', '2024-04-10'),
    ('Febre Amarela', 'Bio-Manguinhos', 'FAM567890', '2025-01-25');

-- Inserção de Carteira de Vacinação
INSERT INTO carteira_vacinacao (paciente_id, vacina_id, funcionario_id, estabelecimento_id, data_aplicacao, dose)
VALUES
    ((SELECT paciente_id FROM pacientes WHERE cpf = '123.456.789-00'), 
     (SELECT vacina_id FROM vacinas WHERE nome = 'Coronavac'),
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '222.333.444-55'),
     (SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'UBS Vila Mariana'),
     '2022-03-15 10:30:00', '1ª Dose'),
    
    ((SELECT paciente_id FROM pacientes WHERE cpf = '123.456.789-00'), 
     (SELECT vacina_id FROM vacinas WHERE nome = 'Coronavac'),
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '222.333.444-55'),
     (SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'UBS Vila Mariana'),
     '2022-04-15 09:45:00', '2ª Dose'),
    
    ((SELECT paciente_id FROM pacientes WHERE cpf = '987.654.321-00'), 
     (SELECT vacina_id FROM vacinas WHERE nome = 'Pfizer COVID-19'),
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '444.555.666-77'),
     (SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'Hospital Municipal Vila Nova Cachoeirinha'),
     '2022-05-10 14:20:00', '1ª Dose'),
    
    ((SELECT paciente_id FROM pacientes WHERE cpf = '987.654.321-00'), 
     (SELECT vacina_id FROM vacinas WHERE nome = 'Pfizer COVID-19'),
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '444.555.666-77'),
     (SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'Hospital Municipal Vila Nova Cachoeirinha'),
     '2022-06-10 15:10:00', '2ª Dose'),
    
    ((SELECT paciente_id FROM pacientes WHERE cpf = '456.789.123-00'), 
     (SELECT vacina_id FROM vacinas WHERE nome = 'Influenza'),
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '222.333.444-55'),
     (SELECT estabelecimento_id FROM estabelecimentos WHERE nome = 'UBS Vila Mariana'),
     '2023-04-20 11:30:00', 'Dose Anual');

-- Inserção de Medicamentos
INSERT INTO medicamentos (nome, principio_ativo, fabricante)
VALUES
    ('Dipirona 500mg', 'Dipirona Sódica', 'EMS'),
    ('Amoxicilina 500mg', 'Amoxicilina', 'Medley'),
    ('Losartana 50mg', 'Losartana Potássica', 'Neo Química'),
    ('Omeprazol 20mg', 'Omeprazol', 'Medley'),
    ('Paracetamol 750mg', 'Paracetamol', 'EMS');

-- Inserção de Prescrições
INSERT INTO prescricoes (atendimento_id, medicamento_id, dosagem, frequencia, duracao)
VALUES
    ((SELECT atendimento_id FROM atendimentos WHERE prontuario_id = (SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '123.456.789-00')) AND diagnostico = 'Enxaqueca tensional'),
     (SELECT medicamento_id FROM medicamentos WHERE nome = 'Dipirona 500mg'),
     '1 comprimido', '8 em 8 horas', '5 dias'),
    
    ((SELECT atendimento_id FROM atendimentos WHERE prontuario_id = (SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '987.654.321-00')) AND diagnostico = 'Angina estável'),
     (SELECT medicamento_id FROM medicamentos WHERE nome = 'Losartana 50mg'),
     '1 comprimido', '1 vez ao dia', 'Uso contínuo'),
    
    ((SELECT atendimento_id FROM atendimentos WHERE prontuario_id = (SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '456.789.123-00')) AND diagnostico = 'Infecção urinária'),
     (SELECT medicamento_id FROM medicamentos WHERE nome = 'Amoxicilina 500mg'),
     '1 comprimido', '8 em 8 horas', '7 dias');

-- Inserção de Exames
INSERT INTO exames (atendimento_id, tipo_exame, data_solicitacao, funcionario_solicitante)
VALUES
    ((SELECT atendimento_id FROM atendimentos WHERE prontuario_id = (SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '123.456.789-00')) AND diagnostico = 'Enxaqueca tensional'),
     'Tomografia de crânio',
     '2023-05-10 10:00:00',
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '111.222.333-44')),
    
    ((SELECT atendimento_id FROM atendimentos WHERE prontuario_id = (SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '987.654.321-00')) AND diagnostico = 'Angina estável'),
     'Eletrocardiograma',
     '2023-06-15 14:30:00',
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '333.444.555-66')),
    
    ((SELECT atendimento_id FROM atendimentos WHERE prontuario_id = (SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '456.789.123-00')) AND diagnostico = 'Infecção urinária'),
     'Exame de urina tipo I',
     '2023-07-20 22:30:00',
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '555.666.777-88')),
    
    ((SELECT atendimento_id FROM atendimentos WHERE prontuario_id = (SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '987.654.321-00')) AND diagnostico = 'Angina estável'),
     'Teste ergométrico',
     '2023-06-16 09:00:00',
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '333.444.555-66'));

-- Inserção de Histórico de Acesso
INSERT INTO historico_acesso (prontuario_id, funcionario_id, tipo_acesso, ip_acesso)
VALUES
    ((SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '123.456.789-00')),
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '111.222.333-44'),
     'Consulta', '192.168.1.100'),
    
    ((SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '987.654.321-00')),
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '333.444.555-66'),
     'Consulta', '192.168.1.101'),
    
    ((SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '456.789.123-00')),
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '555.666.777-88'),
     'Emergência', '192.168.1.102'),
    
    ((SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '123.456.789-00')),
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '222.333.444-55'),
     'Atualização', '192.168.1.103'),
    
    ((SELECT prontuario_id FROM prontuarios WHERE paciente_id = (SELECT paciente_id FROM pacientes WHERE cpf = '987.654.321-00')),
     (SELECT funcionario_id FROM funcionarios WHERE cpf = '444.555.666-77'),
     'Atualização', '192.168.1.104'); 