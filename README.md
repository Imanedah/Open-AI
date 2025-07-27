# 📄 Assistant IA PDF

Ce projet est un assistant IA capable de résumer et d’interroger des fichiers PDF en langage naturel, grâce à OpenAI GPT-4 et une interface Streamlit.

## Fonctionnalités

- Téléversement de PDF
- Résumé automatique
- Q&R sur le contenu
- Téléchargement du résumé
- Interface simple et moderne

## Lancement

```bash
pip install -r requirements.txt
cp .env.example .env  # Mets ta clé OpenAI ici
streamlit run app.py
