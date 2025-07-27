import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

MODEL = "gpt-4o"

def summarize_text(text):
    prompt = f"Résume ce document de façon claire et concise :\n\n{text[:10000]}"
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.5
    )
    return response.choices[0].message.content.strip()

def answer_question(text, question):
    prompt = f"""Voici le contenu d'un document :\n{text[:10000]}\n\nRéponds à la question suivante de façon précise : {question}"""
    response = openai.ChatCompletion.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0.2
    )
    return response.choices[0].message.content.strip()
