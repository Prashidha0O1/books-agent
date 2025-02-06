import os
from dotenv import load_dotenv
from openai import OpenAI

# Load API Key
load_dotenv()

# Initialize OpenAI client
client = OpenAI(api_key=os.getenv("DEEPSEEK_API_KEY"))

def analyze_themes(book_title: str) -> dict:
    """Analyze the core themes and emotional elements of the book"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a literary analyst. Identify the main themes, emotional tone, and key atmospheric elements of the book. Return them in a clear, structured format."},
            {"role": "user", "content": f"Analyze the themes and emotional elements of: {book_title}"}
        ]
    )
    return response.choices[0].message.content

def generate_script(book_title: str, themes: str) -> str:
    """Generate a 100-second narration script with emotional cues"""
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a script writer for short-form video content. Write an engaging 100-second script (approximately 250 words) that includes emotional tone markers and pause indicators in [brackets]. The script should be optimized for a young female narrator."},
            {"role": "user", "content": f"Create a script for {book_title} incorporating these themes: {themes}"}
        ]
    )
    return response.choices[0].message.content

def get_full_summary(book_title: str) -> dict:
    """Generate a complete summary package including themes and script"""
    themes = analyze_themes(book_title)
    script = generate_script(book_title, themes)
    
    return {
        "book_title": book_title,
        "themes": themes,
        "script": script
    }

