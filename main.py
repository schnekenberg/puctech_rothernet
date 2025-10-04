from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from database.session import SessionLocal
from database import crud
from conversions.txt_to_wav import text_to_wav_pt
from conversions.audio_to_text import audio_to_text
from ai.ai_logic import ai_respond
from utils.conversation_helpers import is_conversation_over, extract_order_id
from getters.get_methods import get_order_id
app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Keep track of active WebSocket connections per user
active_connections = {}

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

@app.websocket("/ws/audio/{client_id}")
async def websocket_endpoint(websocket: WebSocket, client_id: str):
    db = SessionLocal()
    await manager.connect(websocket, client_id)

    try:
        while True:
            audio_bytes = await websocket.receive_bytes()
            
            #  Convert audio to text
            user_text = transcrever_audio(tmp_file_path)

            # Store or update client session in DB
            client = crud.get_client(db, client_id)
            if client == -1:
                client = crud.add_client(db, client_id)

            # 3AI generates response
            ai_text = ai_respond(user_text)

            # 4Extract order ID if present
            order_id = get_order_id(user_text)
            if order_id:
                print(f"Detected order ID: {order_id}")

            # Convert AI text to audio
            response_wav_path = text_to_wav_pt(ai_text, output_path=f"responses/{client_id}.wav")
            with open(audio_file_path, "rb") as f:
                audio_data = f.read()
            await manager.send_audio(client_id, audio_data)

            #  Check if conversation is over
            if is_conversation_over(user_text):
                print(f"Conversation ended for {client_id}")
                break

    except WebSocketDisconnect:
        print(f"Client {client_id} disconnected")
    finally:
        manager.disconnect(client_id)
        db.close()
