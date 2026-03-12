from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from openai import OpenAI, OpenAIError
import os

_api_key = os.getenv("OPENAI_API_KEY")
if not _api_key:
    raise RuntimeError("OPENAI_API_KEY environment variable is not set.")

app = FastAPI(title="Universe Dragon Core")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

client = OpenAI(api_key=_api_key)

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
        system_prompt = (
            "You are NOVA, an advanced analytical AI assistant. "
            "Respond in a precise, analytical tone. Begin each reply with 'NOVA 🧠:'."
        )
    elif req.mode.lower() == "dragon":
        system_prompt = (
            "You are DRAGON, a powerful action-oriented AI assistant. "
            "Respond in a bold, decisive tone. Begin each reply with 'DRAGON 🔥:'."
        )
    else:
        raise HTTPException(status_code=400, detail="Invalid mode. Use nova or dragon.")

    try:
        response = client.chat.completions.create(
            model="gpt-4o",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": req.message},
            ],
        )
    except OpenAIError as e:
        raise HTTPException(status_code=502, detail=f"OpenAI API error: {str(e)}")

    reply = response.choices[0].message.content

    return {
        "mode": req.mode,
        "reply": reply
    }
