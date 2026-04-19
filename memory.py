import numpy as np

# Vector size
dimension = 384

# Store memory (text + vector)
memory_store = []

# Fake embedding (lightweight)
def embed(text):
    np.random.seed(abs(hash(text)) % (10**8))  # stable embedding
    return np.random.rand(dimension).astype("float32")

# Add memory
def add_memory(text):
    vec = embed(text)
    memory_store.append((text, vec))

# Cosine similarity
def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

# Search memory
def search_memory(query, k=3):
    if not memory_store:
        return []

    query_vec = embed(query)

    # Compute similarity
    scored = []
    for text, vec in memory_store:
        score = cosine_similarity(query_vec, vec)
        scored.append((score, text))

    # Sort by best match
    scored.sort(reverse=True)

    # Return top k results
    return [text for _, text in scored[:k]]