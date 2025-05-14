FROM node:18-alpine

WORKDIR /app

# Atualizar npm para uma versão compatível com Node 18
RUN npm install -g npm@10.8.2

# Cópia dos arquivos de dependências
COPY package.json package-lock.json* ./

# Instalação das dependências
RUN npm install --legacy-peer-deps

# Cópia do código do aplicativo
COPY . .

# Exposição da porta
EXPOSE 3000

# Comando para iniciar o aplicativo
CMD ["npm", "start"] 