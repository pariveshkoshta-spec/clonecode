from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

# Load MiniLM model locally
model = SentenceTransformer('all-MiniLM-L6-v2')

def get_semantic_similarity(code1: str, code2: str) -> float:
    """Calculates cosine similarity between the embeddings of two code snippets."""
    embeddings = model.encode([code1, code2])
    sim = cosine_similarity([embeddings[0]], [embeddings[1]])[0][0]
    return float(sim)
