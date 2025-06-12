# Projeto Integrador - Chatbot Poliedro
Projeto Integrador Interdisciplinar de alunos do curso de Ciência da Computação do Instituto Mauá de Tecnologia, no primeiro semestre de 2025.

### Integrantes do projeto
| R.A   | Nome |
| -------- | ------- |
| 24.00003-5  | Rafael Alvarez de Carvalho Ruthes    |
| 23.01178-5 | Matheus da Cunha Castilho     |
| 21.01576-7    | Gabriel Borges Silva    |

# Chatbot Backend
Este repositório contém a lógica do backend para um sistema de chatbot, responsável por processar mensagens, interagir com modelos de IA e gerenciar respostas.

# 📂 Estrutura do Projeto
````
text
chatbot/  
├── src/  
│   ├── config/            # Configurações do servidor e integrações  
│   │   ├── openai.js      # Configuração da API da OpenAI  
│   │   └── server.js      # Configuração do servidor (Express)  
│   │  
│   ├── controllers/       # Lógica de manipulação de requisições  
│   │   └── chatbot.js     # Controlador principal do chatbot  
│   │  
│   ├── routes/            # Definição de rotas  
│   │   └── api.js         # Rotas da API (POST /chat, etc.)  
│   │  
│   ├── services/          # Serviços e integrações externas  
│   │   └── openai.js      # Chamadas à API da OpenAI  
│   │  
│   └── utils/             # Utilitários auxiliares  
│       └── helpers.js     # Funções de apoio (tratamento de texto, etc.)  
│  
├── .env.example          # Modelo de variáveis de ambiente  
├── package.json          # Dependências e scripts  
└── server.js             # Ponto de entrada da aplicação  
````

# 🔧 Funcionalidades
Processamento de Mensagens: Recebe mensagens do frontend, envia para o modelo de IA e retorna respostas.

Integração com OpenAI: Utiliza a API da OpenAI (GPT-3.5/4) para gerar respostas contextualizadas.

Gerenciamento de Conversas: Mantém o histórico da conversa para contexto.

API REST: Disponibiliza endpoints para comunicação com o frontend.

# ⚙️ Configuração
Variáveis de Ambiente:

Renomeie .env.example para .env e preencha:
````
text
OPENAI_API_KEY=sua_chave_da_openai  
PORT=3001  # Porta do servidor  
Instalação:

bash
npm install  
Execução:

bash
npm start  # Inicia o servidor
````
  
# 🌐 Rotas da API
POST /api/chat

Body: { "message": "Texto do usuário" }

Resposta: { "reply": "Resposta do chatbot" }

# 📌 Dependências Principais
Express: Framework para o servidor Node.js

OpenAI: Biblioteca oficial para integração com a API da OpenAI

Dotenv: Gerenciamento de variáveis de ambiente

