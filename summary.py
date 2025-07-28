from dotenv import load_dotenv
import os
from openai import OpenAI

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def generate_summary(text):
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Tu es un expert en résumé."},
            {"role": "user", "content": f"Fais un résumé clair et structuré du document suivant :\n{text}"}
        ]
    )
    return response.choices[0].message.content
