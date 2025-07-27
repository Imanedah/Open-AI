import openai

def answer_question(context_chunks, question, openai_api_key):
    openai.api_key = openai_api_key

    context = "\n".join(context_chunks)
    prompt = f"Réponds à la question suivante en te basant uniquement sur ce contexte :\n\n{context}\n\nQuestion : {question}\nRéponse :"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant intelligent qui répond de manière concise et précise."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            max_tokens=500
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Erreur lors de l'appel à l'API : {str(e)}"
