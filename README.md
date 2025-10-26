Bem-vindo ao Projeto Rothernet, um restaurante virtual criado para proporcionar uma experiência de atendimento automatizado e amigável via voz. Desenvolvido com Unity, FastAPI, LangChain, ChromaDB e IA da OpenAI, o projeto permite que clientes conversem com um assistente virtual que entende pedidos, responde perguntas e interage em português com áudio gerado automaticamente pelo backend usando WebSockets e FastAPI.

### Linguagens e Tecnologias Utilizadas
![Python](https://img.shields.io/badge/python-3670A0?style=for-the-badge&logo=python&logoColor=ffdd54) ![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi) ![Unity](https://img.shields.io/badge/unity-%23000000.svg?style=for-the-badge&logo=unity&logoColor=white) ![Postgres](https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white) ![Supabase](https://img.shields.io/badge/Supabase-3ECF8E?style=for-the-badge&logo=supabase&logoColor=white) 
[![LangChain](https://img.shields.io/badge/LangChain-1c3c3c.svg?logo=langchain&logoColor=white)](#) [![OpenAPI](https://img.shields.io/badge/OpenAPI-6BA539?logo=openapiinitiative&logoColor=white)](#)
 
### Desenvolvido por

[@GaiaOcean](https://github.com/Gaiaocean) [@schnekenberg](https://github.com/schnekenberg) [@Ce-22](https://github.com/Ce-22) [@Niikira](https://github.com/Niikira) 



### Funcionalidades

- Atendimento ao cliente por voz: o cliente envia áudios no formato .wav pelo front-end, criado com Unity, e recebe respostas em áudio geradas pela IA da OpenAI.
- Transcrição de áudio: a OpenAI Whisper converte a fala do cliente em texto e captura informações importantes sobre o cliente e seu pedido.
- IA baseada em LangChain: responde seguindo os documentos fornecidos (metodologia RAG), os quais contêm detalhes sobre o cardápio e as regras do restaurante.
- Geração de áudio: respostas da IA são convertidas em áudio com TTS (Text-to-speech) em português.
- Memória de conversa individual: cada cliente mantém seu histórico para continuidade do atendimento a partir do seu User ID.
- Integração com banco de dados: clientes, pedidos e histórico são registrados usando SQLAlchemy.
- Identidade única: Cada cliente possui seu "User ID" (equivalente a um documento de identificação, como o CPF brasileiro), permitindo acessar o histórico de pedidos do cliente no banco de dados.

### Tecnologias utilizadas

- FastAPI: servidor e WebSockets
- Unity: captura e reprodução de áudio
- LangChain + ChromaDB + OpenAI GPT 4.0 Mini: IA para processamento e geração de linguagem natural
- TTS (Text-to-Speech): geração de áudio em português
- OpenAI Whisper: transcrição de áudio para texto
- SQLAlchemy: gerenciamento de clientes, pedidos e históricos.

### Como rodar

1. Clone o Repositório com qualquer um dos métodos abaixo: 
   - SSH: git clone git@github.com:schnekenberg/puctech_rothernet.git
   - HTTPS: git clone https://github.com/schnekenberg/puctech_rothernet.git

2. Instalar dependências:
    - pip install -r requirements.txt

3. Rodar o servidor FastAPI:
    - Utilize o terminal para rodar o comando: uvicorn main:app --reload
