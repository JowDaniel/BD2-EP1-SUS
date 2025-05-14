import React, { useState, useEffect } from 'react';
import {
  Typography,
  Box,
  Card,
  CardContent,
  Grid,
  Paper,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Button,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Tabs,
  Tab,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Snackbar,
  Alert,
  CircularProgress
} from '@mui/material';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider, DatePicker } from '@mui/x-date-pickers';
import axios from 'axios';

function TabPanel(props) {
  const { children, value, index, ...other } = props;

  return (
    <div
      role="tabpanel"
      hidden={value !== index}
      id={`simple-tabpanel-${index}`}
      aria-labelledby={`simple-tab-${index}`}
      {...other}
    >
      {value === index && (
        <Box sx={{ p: 3 }}>
          {children}
        </Box>
      )}
    </div>
  );
}

function VacinacaoManagement() {
  const [tabValue, setTabValue] = useState(0);
  const [vacinas, setVacinas] = useState([]);
  const [carteira, setCarteira] = useState([]);
  const [pacientes, setPacientes] = useState([]);
  const [estabelecimentos, setEstabelecimentos] = useState([]);
  const [funcionarios, setFuncionarios] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [openModal, setOpenModal] = useState(false);
  const [openVacinaModal, setOpenVacinaModal] = useState(false);
  const [selectedPaciente, setSelectedPaciente] = useState('');
  const [alertMessage, setAlertMessage] = useState({ severity: 'info', message: '' });
  const [showAlert, setShowAlert] = useState(false);
  
  const [novaVacina, setNovaVacina] = useState({
    nome: '',
    fabricante: '',
    lote: '',
    validade: null
  });
  
  const [novaVacinacao, setNovaVacinacao] = useState({
    paciente_id: '',
    vacina_id: '',
    funcionario_id: '',
    estabelecimento_id: '',
    data_aplicacao: new Date(),
    dose: '',
    observacoes: ''
  });
  
  useEffect(() => {
    fetchData();
  }, []);
  
  const fetchData = async () => {
    setLoading(true);
    try {
      // No cenário real, buscaríamos todos esses dados da API
      // Por enquanto, simulamos com dados de exemplo
      
      // Vacinas
      const vacinasSimuladas = [
        { vacina_id: '1', nome: 'Coronavac', fabricante: 'Sinovac/Butantan', lote: 'COVA123456', validade: '2024-06-30' },
        { vacina_id: '2', nome: 'Pfizer COVID-19', fabricante: 'Pfizer/BioNTech', lote: 'PFZ789012', validade: '2024-08-15' },
        { vacina_id: '3', nome: 'Tríplice Viral', fabricante: 'Bio-Manguinhos', lote: 'TRV456789', validade: '2025-03-20' },
        { vacina_id: '4', nome: 'Influenza', fabricante: 'Butantan', lote: 'INF234567', validade: '2024-04-10' },
        { vacina_id: '5', nome: 'Febre Amarela', fabricante: 'Bio-Manguinhos', lote: 'FAM567890', validade: '2025-01-25' },
      ];
      setVacinas(vacinasSimuladas);
      
      // Carteira de vacinação
      const carteiraSimulada = [
        { 
          vacinacao_id: '1', 
          nome_paciente: 'Maria Silva', 
          nome_vacina: 'Coronavac', 
          nome_estabelecimento: 'UBS Vila Mariana',
          tipo_estabelecimento: 'POSTO',
          nome_funcionario: 'Enfermeira Patrícia Souza',
          data_aplicacao: '2022-03-15 10:30:00',
          dose: '1ª Dose'
        },
        { 
          vacinacao_id: '2', 
          nome_paciente: 'Maria Silva', 
          nome_vacina: 'Coronavac', 
          nome_estabelecimento: 'UBS Vila Mariana',
          tipo_estabelecimento: 'POSTO',
          nome_funcionario: 'Enfermeira Patrícia Souza',
          data_aplicacao: '2022-04-15 09:45:00',
          dose: '2ª Dose'
        },
        { 
          vacinacao_id: '3', 
          nome_paciente: 'João Santos', 
          nome_vacina: 'Pfizer COVID-19', 
          nome_estabelecimento: 'Hospital Municipal Vila Nova Cachoeirinha',
          tipo_estabelecimento: 'HOSPITAL',
          nome_funcionario: 'Enfermeiro João Silva',
          data_aplicacao: '2022-05-10 14:20:00',
          dose: '1ª Dose'
        },
      ];
      setCarteira(carteiraSimulada);
      
      // Pacientes
      const pacientesSimulados = [
        { paciente_id: '1', nome: 'Maria Silva', cpf: '123.456.789-00', sus_numero: '123456789012345' },
        { paciente_id: '2', nome: 'João Santos', cpf: '987.654.321-00', sus_numero: '987654321098765' },
        { paciente_id: '3', nome: 'Ana Oliveira', cpf: '456.789.123-00', sus_numero: '456789123054321' },
      ];
      setPacientes(pacientesSimulados);
      
      // Estabelecimentos
      const estabelecimentosSimulados = [
        { estabelecimento_id: '1', nome: 'UBS Vila Mariana', tipo: 'POSTO' },
        { estabelecimento_id: '2', nome: 'Hospital Municipal Vila Nova Cachoeirinha', tipo: 'HOSPITAL' },
        { estabelecimento_id: '3', nome: 'UPA Jabaquara', tipo: 'UPA' },
      ];
      setEstabelecimentos(estabelecimentosSimulados);
      
      // Funcionários
      const funcionariosSimulados = [
        { funcionario_id: '1', nome: 'Dr. Roberto Almeida', cargo: 'Médico Clínico Geral' },
        { funcionario_id: '2', nome: 'Enfermeira Patrícia Souza', cargo: 'Enfermeira' },
        { funcionario_id: '3', nome: 'Dr. Marcos Pereira', cargo: 'Médico Cardiologista' },
      ];
      setFuncionarios(funcionariosSimulados);
      
      setLoading(false);
    } catch (err) {
      console.error('Erro ao buscar dados:', err);
      setError('Falha ao carregar dados. Tente novamente mais tarde.');
      setLoading(false);
    }
  };
  
  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };
  
  const handleOpenModal = () => {
    setOpenModal(true);
  };
  
  const handleCloseModal = () => {
    setOpenModal(false);
  };
  
  const handleOpenVacinaModal = () => {
    setOpenVacinaModal(true);
  };
  
  const handleCloseVacinaModal = () => {
    setOpenVacinaModal(false);
  };
  
  const handleVacinaChange = (event) => {
    setNovaVacina({
      ...novaVacina,
      [event.target.name]: event.target.value
    });
  };
  
  const handleVacinacaoChange = (event) => {
    setNovaVacinacao({
      ...novaVacinacao,
      [event.target.name]: event.target.value
    });
  };
  
  const handleVacinaSubmit = () => {
    // Validação simples
    if (!novaVacina.nome || !novaVacina.fabricante || !novaVacina.lote || !novaVacina.validade) {
      setAlertMessage({ severity: 'error', message: 'Preencha todos os campos obrigatórios' });
      setShowAlert(true);
      return;
    }
    
    // No cenário real, enviaríamos para a API
    console.log('Nova vacina:', novaVacina);
    
    // Simulando adição na lista local
    setVacinas([
      ...vacinas,
      {
        vacina_id: Date.now().toString(), // Simulando um novo ID
        ...novaVacina
      }
    ]);
    
    // Resetando o formulário
    setNovaVacina({
      nome: '',
      fabricante: '',
      lote: '',
      validade: null
    });
    
    setAlertMessage({ severity: 'success', message: 'Vacina cadastrada com sucesso!' });
    setShowAlert(true);
    handleCloseVacinaModal();
  };
  
  const handleVacinacaoSubmit = () => {
    // Validação simples
    if (!novaVacinacao.paciente_id || !novaVacinacao.vacina_id || 
        !novaVacinacao.funcionario_id || !novaVacinacao.estabelecimento_id || 
        !novaVacinacao.data_aplicacao || !novaVacinacao.dose) {
      setAlertMessage({ severity: 'error', message: 'Preencha todos os campos obrigatórios' });
      setShowAlert(true);
      return;
    }
    
    // No cenário real, enviaríamos para a API
    console.log('Nova vacinação:', novaVacinacao);
    
    // Buscando detalhes dos relacionamentos
    const paciente = pacientes.find(p => p.paciente_id === novaVacinacao.paciente_id);
    const vacina = vacinas.find(v => v.vacina_id === novaVacinacao.vacina_id);
    const funcionario = funcionarios.find(f => f.funcionario_id === novaVacinacao.funcionario_id);
    const estabelecimento = estabelecimentos.find(e => e.estabelecimento_id === novaVacinacao.estabelecimento_id);
    
    // Simulando adição na lista local
    setCarteira([
      ...carteira,
      {
        vacinacao_id: Date.now().toString(), // Simulando um novo ID
        nome_paciente: paciente.nome,
        nome_vacina: vacina.nome,
        nome_estabelecimento: estabelecimento.nome,
        tipo_estabelecimento: estabelecimento.tipo,
        nome_funcionario: funcionario.nome,
        data_aplicacao: novaVacinacao.data_aplicacao.toISOString(),
        dose: novaVacinacao.dose
      }
    ]);
    
    // Resetando o formulário
    setNovaVacinacao({
      paciente_id: '',
      vacina_id: '',
      funcionario_id: '',
      estabelecimento_id: '',
      data_aplicacao: new Date(),
      dose: '',
      observacoes: ''
    });
    
    setAlertMessage({ severity: 'success', message: 'Vacinação registrada com sucesso!' });
    setShowAlert(true);
    handleCloseModal();
  };
  
  const handlePacienteChange = (event) => {
    setSelectedPaciente(event.target.value);
    // No cenário real, buscaríamos os dados da carteira deste paciente
  };
  
  const handleCloseAlert = () => {
    setShowAlert(false);
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" component="h2" gutterBottom>
        Gestão de Vacinas e Carteira de Vacinação
      </Typography>
      
      <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
        <Tabs value={tabValue} onChange={handleTabChange} aria-label="tabs vacinação">
          <Tab label="Vacinas Disponíveis" />
          <Tab label="Carteira de Vacinação" />
          <Tab label="Consultar por Paciente" />
        </Tabs>
      </Box>
      
      <TabPanel value={tabValue} index={0}>
        <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button 
            variant="contained" 
            color="primary" 
            onClick={handleOpenVacinaModal}
          >
            Cadastrar Nova Vacina
          </Button>
        </Box>
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="tabela de vacinas">
              <TableHead>
                <TableRow>
                  <TableCell><strong>Nome</strong></TableCell>
                  <TableCell><strong>Fabricante</strong></TableCell>
                  <TableCell><strong>Lote</strong></TableCell>
                  <TableCell><strong>Validade</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {vacinas.map((vacina) => (
                  <TableRow key={vacina.vacina_id}>
                    <TableCell>{vacina.nome}</TableCell>
                    <TableCell>{vacina.fabricante}</TableCell>
                    <TableCell>{vacina.lote}</TableCell>
                    <TableCell>{new Date(vacina.validade).toLocaleDateString()}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </TabPanel>
      
      <TabPanel value={tabValue} index={1}>
        <Box sx={{ mb: 2, display: 'flex', justifyContent: 'flex-end' }}>
          <Button 
            variant="contained" 
            color="primary" 
            onClick={handleOpenModal}
          >
            Registrar Nova Vacinação
          </Button>
        </Box>
        
        {loading ? (
          <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
            <CircularProgress />
          </Box>
        ) : error ? (
          <Alert severity="error">{error}</Alert>
        ) : (
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="tabela de vacinações">
              <TableHead>
                <TableRow>
                  <TableCell><strong>Paciente</strong></TableCell>
                  <TableCell><strong>Vacina</strong></TableCell>
                  <TableCell><strong>Dose</strong></TableCell>
                  <TableCell><strong>Data</strong></TableCell>
                  <TableCell><strong>Local</strong></TableCell>
                  <TableCell><strong>Aplicador</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {carteira.map((vacinacao) => (
                  <TableRow key={vacinacao.vacinacao_id}>
                    <TableCell>{vacinacao.nome_paciente}</TableCell>
                    <TableCell>{vacinacao.nome_vacina}</TableCell>
                    <TableCell>{vacinacao.dose}</TableCell>
                    <TableCell>{new Date(vacinacao.data_aplicacao).toLocaleString()}</TableCell>
                    <TableCell>{vacinacao.nome_estabelecimento}</TableCell>
                    <TableCell>{vacinacao.nome_funcionario}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        )}
      </TabPanel>
      
      <TabPanel value={tabValue} index={2}>
        <Box sx={{ mb: 3 }}>
          <FormControl sx={{ minWidth: 300 }}>
            <InputLabel id="filtro-paciente-label">Selecione o paciente</InputLabel>
            <Select
              labelId="filtro-paciente-label"
              id="filtro-paciente"
              value={selectedPaciente}
              label="Selecione o paciente"
              onChange={handlePacienteChange}
            >
              <MenuItem value="">Selecione...</MenuItem>
              {pacientes.map((paciente) => (
                <MenuItem key={paciente.paciente_id} value={paciente.paciente_id}>
                  {paciente.nome} - CPF: {paciente.cpf}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Box>
        
        {selectedPaciente && (
          <>
            <Typography variant="h6" gutterBottom>
              Carteira de Vacinação
            </Typography>
            
            <TableContainer component={Paper}>
              <Table sx={{ minWidth: 650 }} aria-label="tabela de vacinações do paciente">
                <TableHead>
                  <TableRow>
                    <TableCell><strong>Vacina</strong></TableCell>
                    <TableCell><strong>Dose</strong></TableCell>
                    <TableCell><strong>Data</strong></TableCell>
                    <TableCell><strong>Local</strong></TableCell>
                    <TableCell><strong>Aplicador</strong></TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {carteira
                    .filter(v => {
                      const paciente = pacientes.find(p => p.paciente_id === selectedPaciente);
                      return paciente && v.nome_paciente === paciente.nome;
                    })
                    .map((vacinacao) => (
                      <TableRow key={vacinacao.vacinacao_id}>
                        <TableCell>{vacinacao.nome_vacina}</TableCell>
                        <TableCell>{vacinacao.dose}</TableCell>
                        <TableCell>{new Date(vacinacao.data_aplicacao).toLocaleString()}</TableCell>
                        <TableCell>{vacinacao.nome_estabelecimento}</TableCell>
                        <TableCell>{vacinacao.nome_funcionario}</TableCell>
                      </TableRow>
                    ))
                  }
                </TableBody>
              </Table>
            </TableContainer>
            
            {carteira.filter(v => {
              const paciente = pacientes.find(p => p.paciente_id === selectedPaciente);
              return paciente && v.nome_paciente === paciente.nome;
            }).length === 0 && (
              <Box sx={{ mt: 2, p: 2, textAlign: 'center' }}>
                <Typography variant="body1">
                  Este paciente ainda não possui registros de vacinação.
                </Typography>
              </Box>
            )}
          </>
        )}
      </TabPanel>
      
      {/* Modal para cadastrar nova vacinação */}
      <Dialog open={openModal} onClose={handleCloseModal}>
        <DialogTitle>Registrar Nova Vacinação</DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ mt: 1 }}>
            <FormControl fullWidth margin="normal">
              <InputLabel id="paciente-label">Paciente</InputLabel>
              <Select
                labelId="paciente-label"
                id="paciente_id"
                name="paciente_id"
                value={novaVacinacao.paciente_id}
                label="Paciente"
                onChange={handleVacinacaoChange}
              >
                {pacientes.map((paciente) => (
                  <MenuItem key={paciente.paciente_id} value={paciente.paciente_id}>
                    {paciente.nome} - CPF: {paciente.cpf}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <FormControl fullWidth margin="normal">
              <InputLabel id="vacina-label">Vacina</InputLabel>
              <Select
                labelId="vacina-label"
                id="vacina_id"
                name="vacina_id"
                value={novaVacinacao.vacina_id}
                label="Vacina"
                onChange={handleVacinacaoChange}
              >
                {vacinas.map((vacina) => (
                  <MenuItem key={vacina.vacina_id} value={vacina.vacina_id}>
                    {vacina.nome} - Lote: {vacina.lote}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <FormControl fullWidth margin="normal">
              <InputLabel id="dose-label">Dose</InputLabel>
              <Select
                labelId="dose-label"
                id="dose"
                name="dose"
                value={novaVacinacao.dose}
                label="Dose"
                onChange={handleVacinacaoChange}
              >
                <MenuItem value="1ª Dose">1ª Dose</MenuItem>
                <MenuItem value="2ª Dose">2ª Dose</MenuItem>
                <MenuItem value="3ª Dose">3ª Dose</MenuItem>
                <MenuItem value="Dose de Reforço">Dose de Reforço</MenuItem>
                <MenuItem value="Dose Anual">Dose Anual</MenuItem>
                <MenuItem value="Dose Única">Dose Única</MenuItem>
              </Select>
            </FormControl>
            
            <FormControl fullWidth margin="normal">
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DatePicker
                  label="Data de Aplicação"
                  value={novaVacinacao.data_aplicacao}
                  onChange={(newValue) => {
                    setNovaVacinacao({
                      ...novaVacinacao,
                      data_aplicacao: newValue
                    });
                  }}
                  renderInput={(params) => <TextField {...params} />}
                />
              </LocalizationProvider>
            </FormControl>
            
            <FormControl fullWidth margin="normal">
              <InputLabel id="estabelecimento-label">Estabelecimento</InputLabel>
              <Select
                labelId="estabelecimento-label"
                id="estabelecimento_id"
                name="estabelecimento_id"
                value={novaVacinacao.estabelecimento_id}
                label="Estabelecimento"
                onChange={handleVacinacaoChange}
              >
                {estabelecimentos.map((estabelecimento) => (
                  <MenuItem key={estabelecimento.estabelecimento_id} value={estabelecimento.estabelecimento_id}>
                    {estabelecimento.nome} ({estabelecimento.tipo})
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <FormControl fullWidth margin="normal">
              <InputLabel id="funcionario-label">Funcionário Aplicador</InputLabel>
              <Select
                labelId="funcionario-label"
                id="funcionario_id"
                name="funcionario_id"
                value={novaVacinacao.funcionario_id}
                label="Funcionário Aplicador"
                onChange={handleVacinacaoChange}
              >
                {funcionarios.map((funcionario) => (
                  <MenuItem key={funcionario.funcionario_id} value={funcionario.funcionario_id}>
                    {funcionario.nome} - {funcionario.cargo}
                  </MenuItem>
                ))}
              </Select>
            </FormControl>
            
            <TextField
              margin="normal"
              fullWidth
              id="observacoes"
              name="observacoes"
              label="Observações"
              multiline
              rows={3}
              value={novaVacinacao.observacoes}
              onChange={handleVacinacaoChange}
            />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseModal}>Cancelar</Button>
          <Button onClick={handleVacinacaoSubmit} color="primary">Registrar</Button>
        </DialogActions>
      </Dialog>
      
      {/* Modal para cadastrar nova vacina */}
      <Dialog open={openVacinaModal} onClose={handleCloseVacinaModal}>
        <DialogTitle>Cadastrar Nova Vacina</DialogTitle>
        <DialogContent>
          <Box component="form" sx={{ mt: 1 }}>
            <TextField
              margin="normal"
              required
              fullWidth
              id="nome"
              name="nome"
              label="Nome da Vacina"
              value={novaVacina.nome}
              onChange={handleVacinaChange}
            />
            
            <TextField
              margin="normal"
              required
              fullWidth
              id="fabricante"
              name="fabricante"
              label="Fabricante"
              value={novaVacina.fabricante}
              onChange={handleVacinaChange}
            />
            
            <TextField
              margin="normal"
              required
              fullWidth
              id="lote"
              name="lote"
              label="Lote"
              value={novaVacina.lote}
              onChange={handleVacinaChange}
            />
            
            <FormControl fullWidth margin="normal">
              <LocalizationProvider dateAdapter={AdapterDateFns}>
                <DatePicker
                  label="Data de Validade"
                  value={novaVacina.validade}
                  onChange={(newValue) => {
                    setNovaVacina({
                      ...novaVacina,
                      validade: newValue
                    });
                  }}
                  renderInput={(params) => <TextField {...params} />}
                />
              </LocalizationProvider>
            </FormControl>
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={handleCloseVacinaModal}>Cancelar</Button>
          <Button onClick={handleVacinaSubmit} color="primary">Cadastrar</Button>
        </DialogActions>
      </Dialog>
      
      <Snackbar 
        open={showAlert} 
        autoHideDuration={6000} 
        onClose={handleCloseAlert}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'center' }}
      >
        <Alert onClose={handleCloseAlert} severity={alertMessage.severity} sx={{ width: '100%' }}>
          {alertMessage.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default VacinacaoManagement; 