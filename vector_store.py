from sentence_transformers import SentenceTransformer
import faiss
import numpy as np

def build_faiss_index(text, chunk_size=500):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    embeddings = model.encode(chunks)
    index = faiss.IndexFlatL2(len(embeddings[0]))
    index.add(np.array(embeddings))
    return index, chunks

def search_index(index, chunks, query, top_k=5):
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([query])
    distances, indices = index.search(np.array(query_embedding), top_k)
    return [chunks[i] for i in indices[0]]
