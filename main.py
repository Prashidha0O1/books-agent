
import os
import uvicorn
from fastapi import FastAPI
from dotenv import load_dotenv
from summarizer import get_summary
from tts import generate_audio

# Load API keys from .env
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Books Agent API is running!"}

@app.get("/summarize/")
def summarize_book(title: str):
    """Returns a GPT-4 summary of the book"""
    summary = get_summary(title)
    return {"book": title, "summary": summary}

@app.get("/tts/")
def get_audio(title: str):
    """Converts summary to speech"""
    summary = get_summary(title)
    audio_file = generate_audio(summary)
    return {"message": "Audio generated!", "file": audio_file}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
