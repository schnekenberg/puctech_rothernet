import os
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware

from database.session import SessionLocal
from database import crud
from conversions.txt_to_wav import text_to_wav_pt
from conversions.wav_to_txt import transcrever_audio
from ai.ai_logic import ai_respond
from utils.conversation_helpers import is_conversation_over
from getters.get_methods import get_order_id

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Gerencia conexões WebSocket ativas
class ConnectionManager:
    def __init__(self):
        self.connections = {}

    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.connections[client_id] = websocket

    def disconnect(self, client_id: str):
        self.connections.pop(client_id, None)

    async def send_audio(self, client_id: str, audio_bytes: bytes):
        if client_id in self.connections:
            await self.connections[client_id].send_bytes(audio_bytes)

manager = ConnectionManager()

os.makedirs("audios/received_audio", exist_ok=True)
os.makedirs("audios/audio_responses", exist_ok=True)

@app.websocket("/ws/audio/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    db = SessionLocal()
    await manager.connect(websocket, client_id)

    try:
        while True:
            # 1. Recebe áudio do Unity
            audio_bytes = await websocket.receive_bytes()
            tmp_file_path = f"audios/received_audio/{client_id}.wav"
            with open(tmp_file_path, "wb") as f:
                f.write(audio_bytes)

            # 2. Converte áudio em texto
            user_text = transcrever_audio(tmp_file_path)

            # 3. Cria ou atualiza cliente no banco
            client = crud.get_client(db, client_id)
            if client == -1:
                client = crud.add_client(db, client_id)

            # 4. IA gera resposta
            ai_text = ai_response(user_text)  #nao sei o nome da funcao mas é só pra saber o fluxo

            # 5. Detecta ID de pedido se houver
            order_id = get_order_id(user_text)
            if order_id:
                print(f"Detected order ID: {order_id}")

            # 6. Converte resposta da IA em áudio
            response_wav_path = f"audios/audio_responses/{client_id}.wav"
            text_to_wav_pt(ai_text, output_path=response_wav_path)
            with open(response_wav_path, "rb") as f:
                audio_data = f.read()

            # 7. Envia áudio de volta ao cliente
            await manager.send_audio(client_id, audio_data)

            # 8. Verifica se a conversa terminou
            if is_interaction_over(user_text):
                print(f"Conversation ended for {client_id}")
                break

    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
    finally:
        manager.disconnect(client_id)
        db.close()
