import faiss
import numpy as np

# Vector size
dimension = 384

# FAISS index
index = faiss.IndexFlatL2(dimension)

# Store text
memory_store = []

# Fake embedding (lightweight)
def embed(text):
    return np.random.rand(dimension).astype("float32")

# Add memory
def add_memory(text):
    vec = embed(text)
    index.add(np.array([vec]))
    memory_store.append(text)

# Search memory
def search_memory(query, k=2):
    if len(memory_store) == 0:
        return []

    vec = embed(query)
    D, I = index.search(np.array([vec]), k)

    return [memory_store[i] for i in I[0] if i < len(memory_store)]