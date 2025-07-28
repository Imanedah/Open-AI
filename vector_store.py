from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import streamlit as st

@st.cache_resource
def load_sentence_model():
    """
    Charge le modèle de sentence transformers avec cache
    """
    return SentenceTransformer('all-MiniLM-L6-v2')

def build_faiss_index(text, chunk_size=800, overlap=100):
    """
    Construit un index FAISS avec découpage intelligent du texte
    """
    try:
        model = load_sentence_model()
        
        # Découpage intelligent avec chevauchement
        chunks = []
        for i in range(0, len(text), chunk_size - overlap):
            chunk = text[i:i + chunk_size]
            if chunk.strip():  # Éviter les chunks vides
                chunks.append(chunk.strip())
        
        if not chunks:
            raise Exception("Aucun chunk de texte créé")
        
        # Générer les embeddings
        embeddings = model.encode(chunks, show_progress_bar=False)
        
        # Créer l'index FAISS
        dimension = len(embeddings[0])
        index = faiss.IndexFlatL2(dimension)
        index.add(np.array(embeddings).astype('float32'))
        
        return index, chunks
        
    except Exception as e:
        raise Exception(f"Erreur lors de la construction de l'index: {str(e)}")

def search_index(index, chunks, query, top_k=5):
    """
    Recherche dans l'index FAISS avec gestion d'erreurs
    """
    try:
        model = load_sentence_model()
        
        # Encoder la requête
        query_embedding = model.encode([query], show_progress_bar=False)
        
        # Rechercher dans l'index
        distances, indices = index.search(
            np.array(query_embedding).astype('float32'), 
            min(top_k, len(chunks))  # Ne pas chercher plus de chunks qu'il n'y en a
        )
        
        # Retourner les chunks pertinents
        relevant_chunks = []
        for i in indices[0]:
            if i < len(chunks):  # Vérification de sécurité
                relevant_chunks.append(chunks[i])
        
        return relevant_chunks
        
    except Exception as e:
        # En cas d'erreur, retourner les premiers chunks
        return chunks[:top_k] if chunks else [query]