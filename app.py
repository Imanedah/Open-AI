import streamlit as st
from pdf_handler import extract_text_from_pdf
from vector_store import build_faiss_index, search_index
from qa_engine import answer_question
from summary import generate_summary
from utils import convert_text_to_pdf, convert_text_to_csv

st.set_page_config(page_title="Assistant IA PDF", layout="wide")

st.title("📄 Assistant IA pour documents PDF")

openai_api_key = st.text_input("🔑 Clé API OpenAI", type="password")

uploaded_files = st.file_uploader("📤 Chargez un ou plusieurs fichiers PDF", type="pdf", accept_multiple_files=True)

question = st.text_input("❓ Posez une question sur le contenu")

if st.button("Poser la question"):
    if not openai_api_key:
        st.error("Veuillez entrer votre clé API OpenAI.")
    elif not uploaded_files:
        st.error("Veuillez d'abord charger au moins un fichier PDF.")
    elif not question:
        st.error("Veuillez poser une question.")
    else:
        all_text = ""
        for file in uploaded_files:
            all_text += extract_text_from_pdf(file)

        with st.spinner("🔍 Analyse en cours..."):
            index, chunks = build_faiss_index(all_text)
            context_chunks = search_index(index, chunks, question)
            response = answer_question(context_chunks, question, openai_api_key)

        st.success("✅ Réponse générée :")
        st.write(response)

if st.button("📑 Générer un résumé"):
    if not openai_api_key:
        st.error("Veuillez entrer votre clé API OpenAI.")
    elif not uploaded_files:
        st.error("Veuillez d'abord charger au moins un fichier PDF.")
    else:
        all_text = ""
        for file in uploaded_files:
            all_text += extract_text_from_pdf(file)

        with st.spinner("📝 Résumé en cours..."):
            summary = generate_summary(all_text, openai_api_key)
        st.success("✅ Résumé généré :")
        st.write(summary)

        col1, col2 = st.columns(2)
        with col1:
            st.download_button("📥 Télécharger en PDF", data=convert_text_to_pdf(summary), file_name="resume.pdf")
        with col2:
            st.download_button("📥 Télécharger en CSV", data=convert_text_to_csv(summary), file_name="resume.csv")
