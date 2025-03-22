import os
import csv
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# We'll reuse your existing Gemini call from open_requests.py
from functions.open_requests import get_chat_response

# Global variables to store the FAISS index and associated text data
embedding_model = None
index = None
documents = []

def init_rag(csv_path="E://SpeakAI/backend/reva_webscraped_data_filtered.csv"):
    """
    Initialize the RAG system by:
    1. Reading the CSV (no URL column).
    2. Embedding each row's text using SentenceTransformers.
    3. Building a FAISS index for vector similarity search.
    """
    global embedding_model, index, documents

    # Load an embedding model from SentenceTransformers
    # (You can pick any model you like on Hugging Face)
    if embedding_model is None:
        embedding_model = SentenceTransformer('multi-qa-MiniLM-L6-cos-v1')

    # Read CSV rows (Header Level, Header Text, Content)
    rows = []
    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Combine relevant columns into one text chunk
            combined_text = f"{row['Header Level']} - {row['Header Text']}:\n{row['Content']}"
            rows.append(combined_text)

    documents = rows  # Keep a copy so we can map back after search

    # Embed all rows
    embeddings = embedding_model.encode(rows, convert_to_numpy=True)

    # Build a FAISS index
    dimension = embeddings.shape[1]
    index = faiss.IndexFlatL2(dimension)
    index.add(embeddings)

def search_reva_data(query, top_k=3):
    """
    Search for the top_k most relevant chunks in the CSV data
    based on the user's query.
    """
    global embedding_model, index, documents

    # Edge case: if index not initialized
    if index is None or embedding_model is None:
        raise RuntimeError("RAG system not initialized. Call init_rag() first.")

    # Convert query to embedding
    query_emb = embedding_model.encode([query], convert_to_numpy=True)
    # Perform vector search in FAISS
    distances, indices = index.search(query_emb, top_k)

    # Retrieve the matched text chunks
    results = [documents[i] for i in indices[0]]
    return results

def generate_rag_response(user_query):
    """
    1. Retrieve the top relevant content from the CSV using vector search.
    2. Construct a prompt that includes the retrieved text as context.
    3. Call get_chat_response() (Gemini) to generate a final answer.
    """
    # Get the top relevant data
    relevant_texts = search_reva_data(user_query, top_k=3)
    # Combine them into a single context string
    context = "\n\n".join(relevant_texts)

    # Build a short prompt that instructs Gemini to use the provided context
    # and answer in under 50 words (or any other style constraints).
    prompt = (
        "You are Speak AI, a friendly assistant. Use the following context about REVA University to answer "
        "the user's question accurately. Keep your answer under 50 words.\n\n"
        f"Context:\n{context}\n\n"
        f"Question: {user_query}\n\n"
        "Answer:"
    )

    # Use the existing Gemini function to get a response
    response = get_chat_response(prompt)
    return response
