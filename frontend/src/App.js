import React, { useState, useEffect } from 'react';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { 
  Box, 
  Container, 
  Typography, 
  Paper, 
  CircularProgress,
  AppBar,
  Toolbar,
  Button,
  Tab,
  Tabs,
  List,
  ListItem,
  ListItemText,
  Divider,
  TextField,
  Grid,
  Card,
  CardContent,
  Alert,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow
} from '@mui/material';
import LocalHospitalIcon from '@mui/icons-material/LocalHospital';
import axios from 'axios';
import EstabelecimentosList from './components/EstabelecimentosList';
import VacinacaoManagement from './components/VacinacaoManagement';

const theme = createTheme({
  palette: {
    primary: {
      main: '#2196f3', // Azul SUS
    },
    secondary: {
      main: '#4caf50', // Verde
    },
  },
});

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

function a11yProps(index) {
  return {
    id: `simple-tab-${index}`,
    'aria-controls': `simple-tabpanel-${index}`,
  };
}

function App() {
  const [backendStatus, setBackendStatus] = useState('Conectando...');
  const [tabValue, setTabValue] = useState(0);
  const [pacientes, setPacientes] = useState([]);
  const [formData, setFormData] = useState({
    nome: '',
    cpf: '',
    data_nascimento: '',
    sexo: '',
    sus_numero: '',
    endereco: '',
    telefone: '',
    email: '',
    tipo_sanguineo: ''
  });
  const [submitStatus, setSubmitStatus] = useState({ success: false, error: false, message: '' });

  // Carregar status do backend
  useEffect(() => {
    const checkBackendStatus = async () => {
      try {
        const response = await axios.get('http://localhost:8000/');
        if (response.data.status === 'online') {
          setBackendStatus('Conectado');
          // Carregar pacientes se conectado com sucesso
          fetchPacientes();
        } else {
          setBackendStatus('Erro: Status inesperado');
        }
      } catch (error) {
        console.error('Erro ao conectar com o backend:', error);
        setBackendStatus('Erro de conexão');
      }
    };

    checkBackendStatus();
    // Verificar status a cada 30 segundos
    const interval = setInterval(checkBackendStatus, 30000);
    
    return () => clearInterval(interval);
  }, []);

  // Buscar pacientes 
  const fetchPacientes = async () => {
    try {
      const response = await axios.get('http://localhost:8000/api/v1/pacientes/');
      // Como sabemos que a API retorna um placeholder, vamos criar dados de exemplo
      // No futuro, você substituiria isso pela resposta real da API
      setPacientes([
        { id: 1, nome: 'Maria Silva', cpf: '123.456.789-00', sus_numero: '123456789012345', data_nascimento: '1980-05-15' },
        { id: 2, nome: 'João Santos', cpf: '987.654.321-00', sus_numero: '987654321098765', data_nascimento: '1975-10-20' },
        { id: 3, nome: 'Ana Oliveira', cpf: '456.789.123-00', sus_numero: '456789123054321', data_nascimento: '1990-03-25' },
      ]);
    } catch (error) {
      console.error('Erro ao buscar pacientes:', error);
    }
  };

  const handleTabChange = (event, newValue) => {
    setTabValue(newValue);
  };

  const handleFormChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value
    });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      // Em um cenário real, enviaria para o backend:
      // await axios.post('http://localhost:8000/api/v1/pacientes/', formData);
      
      // Como é um exemplo, apenas simulamos o sucesso
      console.log('Dados enviados:', formData);
      setSubmitStatus({
        success: true,
        error: false,
        message: 'Paciente cadastrado com sucesso!'
      });
      
      // Resetar formulário
      setFormData({
        nome: '',
        cpf: '',
        data_nascimento: '',
        sexo: '',
        sus_numero: '',
        endereco: '',
        telefone: '',
        email: '',
        tipo_sanguineo: ''
      });
      
      // Adicionar o novo paciente à lista (simulação)
      setPacientes([...pacientes, {
        id: pacientes.length + 1,
        nome: formData.nome,
        cpf: formData.cpf,
        sus_numero: formData.sus_numero,
        data_nascimento: formData.data_nascimento
      }]);
      
    } catch (error) {
      console.error('Erro ao cadastrar paciente:', error);
      setSubmitStatus({
        success: false,
        error: true,
        message: 'Erro ao cadastrar paciente. Tente novamente.'
      });
    }
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      
      <AppBar position="static">
        <Toolbar>
          <LocalHospitalIcon sx={{ mr: 2 }} />
          <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
            SUS - Sistema de Compartilhamento de Dados
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Typography variant="body2" sx={{ mr: 2 }}>
              Status: <strong>{backendStatus}</strong>
            </Typography>
            {backendStatus === 'Conectando...' && <CircularProgress size={20} color="inherit" />}
          </Box>
        </Toolbar>
      </AppBar>
      
      <Container maxWidth="lg">
        <Box sx={{ width: '100%', mt: 3 }}>
          <Box sx={{ borderBottom: 1, borderColor: 'divider' }}>
            <Tabs value={tabValue} onChange={handleTabChange} aria-label="basic tabs example">
              <Tab label="Início" {...a11yProps(0)} />
              <Tab label="Pacientes" {...a11yProps(1)} />
              <Tab label="Cadastro" {...a11yProps(2)} />
              <Tab label="Estabelecimentos" {...a11yProps(3)} />
              <Tab label="Vacinas" {...a11yProps(4)} />
            </Tabs>
          </Box>
          
          <TabPanel value={tabValue} index={0}>
            <Typography variant="h4" component="h1" gutterBottom>
              Sistema de Compartilhamento de Dados de Pacientes do SUS
            </Typography>
            
            <Paper elevation={3} sx={{ p: 3, mt: 3 }}>
              <Typography variant="h5" component="h2" gutterBottom>
                Bem-vindo ao Sistema
              </Typography>
              <Typography variant="body1" paragraph>
                Esta é a interface do sistema para centralizar e compartilhar dados de pacientes
                (carteirinhas de vacinação e prontuários médicos) entre postos de saúde e hospitais do SUS.
              </Typography>
              <Typography variant="body1">
                Use as abas acima para navegar pelo sistema:
              </Typography>
              <List>
                <ListItem>
                  <ListItemText 
                    primary="Pacientes" 
                    secondary="Visualize a lista de pacientes cadastrados no sistema" 
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Cadastro" 
                    secondary="Adicione novos pacientes ao sistema" 
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Estabelecimentos" 
                    secondary="Consulte a lista de Hospitais, UBS e UPAs" 
                  />
                </ListItem>
                <ListItem>
                  <ListItemText 
                    primary="Vacinas" 
                    secondary="Gerencie vacinas e carteiras de vacinação" 
                  />
                </ListItem>
              </List>
            </Paper>
          </TabPanel>
          
          <TabPanel value={tabValue} index={1}>
            <Typography variant="h5" component="h2" gutterBottom>
              Pacientes Cadastrados
            </Typography>
            
            {pacientes.length > 0 ? (
              <TableContainer component={Paper}>
                <Table sx={{ minWidth: 650 }} aria-label="tabela de pacientes">
                  <TableHead>
                    <TableRow>
                      <TableCell><strong>Nome</strong></TableCell>
                      <TableCell><strong>CPF</strong></TableCell>
                      <TableCell><strong>Cartão SUS</strong></TableCell>
                      <TableCell><strong>Data de Nascimento</strong></TableCell>
                      <TableCell><strong>Ações</strong></TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {pacientes.map((paciente) => (
                      <TableRow key={paciente.id}>
                        <TableCell>{paciente.nome}</TableCell>
                        <TableCell>{paciente.cpf}</TableCell>
                        <TableCell>{paciente.sus_numero}</TableCell>
                        <TableCell>{new Date(paciente.data_nascimento).toLocaleDateString()}</TableCell>
                        <TableCell>
                          <Button 
                            size="small" 
                            variant="outlined" 
                            color="primary" 
                            sx={{ mr: 1 }}
                          >
                            Prontuário
                          </Button>
                          <Button 
                            size="small" 
                            variant="outlined" 
                            color="secondary"
                          >
                            Vacinas
                          </Button>
                        </TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            ) : (
              <Alert severity="info">
                Nenhum paciente cadastrado até o momento.
              </Alert>
            )}
          </TabPanel>
          
          <TabPanel value={tabValue} index={2}>
            <Typography variant="h5" component="h2" gutterBottom>
              Cadastro de Pacientes
            </Typography>
            
            <Paper elevation={3} sx={{ p: 3 }}>
              {submitStatus.success && (
                <Alert severity="success" sx={{ mb: 2 }}>
                  {submitStatus.message}
                </Alert>
              )}
              
              {submitStatus.error && (
                <Alert severity="error" sx={{ mb: 2 }}>
                  {submitStatus.message}
                </Alert>
              )}
              
              <Box component="form" onSubmit={handleSubmit}>
                <Grid container spacing={2}>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      required
                      fullWidth
                      id="nome"
                      label="Nome Completo"
                      name="nome"
                      value={formData.nome}
                      onChange={handleFormChange}
                      margin="normal"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      required
                      fullWidth
                      id="cpf"
                      label="CPF"
                      name="cpf"
                      value={formData.cpf}
                      onChange={handleFormChange}
                      placeholder="000.000.000-00"
                      margin="normal"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      required
                      fullWidth
                      id="data_nascimento"
                      label="Data de Nascimento"
                      name="data_nascimento"
                      type="date"
                      value={formData.data_nascimento}
                      onChange={handleFormChange}
                      margin="normal"
                      InputLabelProps={{ shrink: true }}
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      required
                      fullWidth
                      select
                      id="sexo"
                      label="Sexo"
                      name="sexo"
                      value={formData.sexo}
                      onChange={handleFormChange}
                      margin="normal"
                      SelectProps={{
                        native: true,
                      }}
                    >
                      <option value=""></option>
                      <option value="M">Masculino</option>
                      <option value="F">Feminino</option>
                      <option value="O">Outro</option>
                    </TextField>
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      required
                      fullWidth
                      id="sus_numero"
                      label="Número do Cartão SUS"
                      name="sus_numero"
                      value={formData.sus_numero}
                      onChange={handleFormChange}
                      margin="normal"
                    />
                  </Grid>
                  <Grid item xs={12}>
                    <TextField
                      fullWidth
                      id="endereco"
                      label="Endereço Completo"
                      name="endereco"
                      value={formData.endereco}
                      onChange={handleFormChange}
                      margin="normal"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      id="telefone"
                      label="Telefone"
                      name="telefone"
                      value={formData.telefone}
                      onChange={handleFormChange}
                      margin="normal"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      id="email"
                      label="E-mail"
                      name="email"
                      type="email"
                      value={formData.email}
                      onChange={handleFormChange}
                      margin="normal"
                    />
                  </Grid>
                  <Grid item xs={12} sm={6}>
                    <TextField
                      fullWidth
                      id="tipo_sanguineo"
                      label="Tipo Sanguíneo"
                      name="tipo_sanguineo"
                      value={formData.tipo_sanguineo}
                      onChange={handleFormChange}
                      margin="normal"
                      select
                      SelectProps={{
                        native: true,
                      }}
                    >
                      <option value=""></option>
                      <option value="A+">A+</option>
                      <option value="A-">A-</option>
                      <option value="B+">B+</option>
                      <option value="B-">B-</option>
                      <option value="AB+">AB+</option>
                      <option value="AB-">AB-</option>
                      <option value="O+">O+</option>
                      <option value="O-">O-</option>
                    </TextField>
                  </Grid>
                </Grid>
                
                <Box sx={{ mt: 3, display: 'flex', justifyContent: 'flex-end' }}>
                  <Button
                    type="submit"
                    variant="contained"
                    color="primary"
                  >
                    Cadastrar Paciente
                  </Button>
                </Box>
              </Box>
            </Paper>
          </TabPanel>
          
          <TabPanel value={tabValue} index={3}>
            <EstabelecimentosList />
          </TabPanel>
          
          <TabPanel value={tabValue} index={4}>
            <VacinacaoManagement />
          </TabPanel>
        </Box>
      </Container>
    </ThemeProvider>
  );
}

export default App;