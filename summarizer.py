
import openai
import os
from dotenv import load_dotenv

# Load API Key
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

def get_summary(book_title: str):
    """Generate a summary using GPT-4"""
    prompt = f"Summarize the book '{book_title}' in a way that entices readers without revealing major spoilers."
    
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    )
    
    return response["choices"][0]["message"]["content"]

