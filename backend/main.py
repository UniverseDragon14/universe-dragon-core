from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os

app = FastAPI(title="Universe Dragon Core")

# ===== Request Model =====
class ChatRequest(BaseModel):
    mode: str
    message: str

# ===== Root Test =====
@app.get("/")
def home():
    return {
        "status": "online",
        "system": "Universe Dragon Core 🔥"
    }

# ===== Chat Endpoint =====
@app.post("/api/chat")
def chat(req: ChatRequest):
    
    if req.mode.lower() == "nova":
        reply = f"NOVA 🧠: Analyzing -> {req.message}"
    
    elif req.mode.lower() == "dragon":
        reply = f"DRAGON 🔥: Executing -> {req.message}"
    
    else:
        raise HTTPException(status_code=400, detail="Invalid mode. Use nova or dragon.")

    return {
        "mode": req.mode,
        "reply": reply
    }
