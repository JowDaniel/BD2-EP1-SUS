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
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Snackbar,
  Alert,
  CircularProgress
} from '@mui/material';
import axios from 'axios';

function EstabelecimentosList() {
  const [estabelecimentos, setEstabelecimentos] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filtroTipo, setFiltroTipo] = useState('');
  
  useEffect(() => {
    fetchEstabelecimentos();
  }, [filtroTipo]);
  
  const fetchEstabelecimentos = async () => {
    setLoading(true);
    try {
      let url = 'http://localhost:8000/api/v1/estabelecimentos/';
      
      if (filtroTipo) {
        url = `http://localhost:8000/api/v1/estabelecimentos/tipo/${filtroTipo}`;
      }
      
      const response = await axios.get(url);
      
      // No cenário real, usaríamos response.data
      // Simulando dados para teste
      const dadosTeste = [
        { 
          estabelecimento_id: '1', 
          nome: 'Hospital Municipal São Paulo', 
          tipo: 'HOSPITAL', 
          endereco: 'Av. Paulista, 1000, São Paulo, SP', 
          telefone: '(11) 3333-4444',
          horario_funcionamento: '24 horas'
        },
        { 
          estabelecimento_id: '2', 
          nome: 'UBS Vila Mariana', 
          tipo: 'POSTO', 
          endereco: 'Rua Domingos de Morais, 1200, São Paulo, SP', 
          telefone: '(11) 5555-6666',
          horario_funcionamento: 'Segunda a Sexta, 7h às 19h'
        },
        { 
          estabelecimento_id: '3', 
          nome: 'UPA Jabaquara', 
          tipo: 'UPA', 
          endereco: 'Rua das Rosas, 86, São Paulo, SP', 
          telefone: '(11) 7777-8888',
          horario_funcionamento: '24 horas'
        },
      ];
      
      if (filtroTipo && filtroTipo !== '') {
        setEstabelecimentos(dadosTeste.filter(est => est.tipo === filtroTipo));
      } else {
        setEstabelecimentos(dadosTeste);
      }
      
      setLoading(false);
    } catch (err) {
      console.error('Erro ao buscar estabelecimentos:', err);
      setError('Falha ao carregar estabelecimentos. Tente novamente mais tarde.');
      setLoading(false);
    }
  };
  
  const handleFiltroChange = (event) => {
    setFiltroTipo(event.target.value);
  };

  return (
    <Box sx={{ mt: 3 }}>
      <Typography variant="h5" component="h2" gutterBottom>
        Estabelecimentos de Saúde
      </Typography>
      
      <Box sx={{ mb: 3 }}>
        <FormControl sx={{ minWidth: 200 }}>
          <InputLabel id="filtro-tipo-label">Filtrar por tipo</InputLabel>
          <Select
            labelId="filtro-tipo-label"
            id="filtro-tipo"
            value={filtroTipo}
            label="Filtrar por tipo"
            onChange={handleFiltroChange}
          >
            <MenuItem value="">Todos</MenuItem>
            <MenuItem value="HOSPITAL">Hospitais</MenuItem>
            <MenuItem value="POSTO">UBS (Postos de Saúde)</MenuItem>
            <MenuItem value="UPA">UPA</MenuItem>
            <MenuItem value="OUTRO">Outros</MenuItem>
          </Select>
        </FormControl>
      </Box>
      
      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', mt: 4 }}>
          <CircularProgress />
        </Box>
      ) : error ? (
        <Alert severity="error">{error}</Alert>
      ) : (
        <>
          <TableContainer component={Paper}>
            <Table sx={{ minWidth: 650 }} aria-label="tabela de estabelecimentos">
              <TableHead>
                <TableRow>
                  <TableCell><strong>Nome</strong></TableCell>
                  <TableCell><strong>Tipo</strong></TableCell>
                  <TableCell><strong>Endereço</strong></TableCell>
                  <TableCell><strong>Telefone</strong></TableCell>
                  <TableCell><strong>Horário</strong></TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {estabelecimentos.map((estabelecimento) => (
                  <TableRow key={estabelecimento.estabelecimento_id}>
                    <TableCell>{estabelecimento.nome}</TableCell>
                    <TableCell>
                      {estabelecimento.tipo === 'HOSPITAL' && 'Hospital'}
                      {estabelecimento.tipo === 'POSTO' && 'UBS (Posto de Saúde)'}
                      {estabelecimento.tipo === 'UPA' && 'UPA'}
                      {estabelecimento.tipo === 'OUTRO' && 'Outro'}
                    </TableCell>
                    <TableCell>{estabelecimento.endereco}</TableCell>
                    <TableCell>{estabelecimento.telefone}</TableCell>
                    <TableCell>{estabelecimento.horario_funcionamento}</TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
          
          {estabelecimentos.length === 0 && (
            <Box sx={{ mt: 2, p: 2, textAlign: 'center' }}>
              <Typography variant="body1">
                Nenhum estabelecimento encontrado com os filtros atuais.
              </Typography>
            </Box>
          )}
        </>
      )}
    </Box>
  );
}

export default EstabelecimentosList; 