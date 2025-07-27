import openai

def generate_summary(text, openai_api_key):
    openai.api_key = openai_api_key

    prompt = f"Voici un texte à résumer de façon claire, précise et bien structurée :\n\n{text}\n\nRésumé :"

    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Tu es un assistant qui génère des résumés professionnels et structurés."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.4,
            max_tokens=700
        )
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        return f"Erreur lors de l'appel à l'API : {str(e)}"
