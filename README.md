Bem-vindo ao Rothnet, um restaurante virtual criado para proporcionar uma experiência de atendimento automatizado e amigável via voz. Desenvolvido com Unity, FastAPI, LangChain, ChromaDB e IA da OpenAI, o projeto permite que clientes conversem com um assistente virtual que entende pedidos, responde perguntas e interage em português com áudio gerado automaticamente pelo backend usando WebSockets e FastAPI.

### Funcionalidades:

- Atendimento ao cliente por voz: o cliente envia áudios no formato .wav pelo front-end, criado com Unity,e recebe respostas em áudio geradas pela ia da openai.
- Transcrição de áudio: a OpenAI Whisper converte a fala do cliente em texto e captura informações importantes sobre o cliente e seu pedido.
- IA baseada em LangChain: responde seguindo o RAG criado, o qual contém detalhes sobre o cardápio e as regras do restaurante.
- Geração de áudio: respostas da IA são convertidas em áudio com TTS(Text-to-speech) em português.
- Memória de conversa individual: cada cliente mantém seu histórico para continuidade do atendimento a partir do seu user id.
- Integração com banco de dados: clientes, pedidos e histórico são registrados usando SQLAlchemy.
- Identidade única: Cada cliente possui seu "user id"(equivalente ao CPF brasileiro), permitindo acessar o histórico de pedidos do cliente no banco de dados.

### Tecnologias utilizadas

- FastAPI: servidor e WebSockets
- Unity: captura e reprodução de áudio
- LangChain + ChromaDB + OpenAI GPT : IA para processamento e geração de linguagem natural
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
    - uvicorn main:app --reload
