import os
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from dotenv import load_dotenv
from summarizer import get_summary
from tts import generate_audio
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI(
    title="Books AI Agent",
    description="An AI agent that provides book summaries and audio versions",
    version="1.0.0"
)

# Add this after creating the FastAPI app
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # Add your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files directory for serving audio files
app.mount("/static", StaticFiles(directory="static"), name="static")

class SummaryResponse(BaseModel):
    book: str
    summary: str

class AudioResponse(BaseModel):
    book: str
    summary: str
    audio_url: str

@app.get("/")
def read_root():
    return {"message": "Books Agent API is running!"}

@app.get("/summarize/{title}", response_model=SummaryResponse)
async def summarize_book(title: str):
    """Returns a GPT-4 summary of the book"""
    try:
        summary = get_summary(title)
        return {"book": title, "summary": summary}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/tts/{title}", response_model=AudioResponse)
async def get_audio(title: str):
    """Generates and returns audio summary"""
    try:
        summary = get_summary(title)
        audio_file = generate_audio(summary)
        audio_url = f"/static/audio/{audio_file}"
        return {
            "book": title,
            "summary": summary,
            "audio_url": audio_url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
