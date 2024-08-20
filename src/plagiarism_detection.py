import numpy as np

def calculate_similarity(features1, features2, threshold=0.8):
    """Calculate similarity between two sets of features using cosine similarity."""
    similarities = []
    for feat1, feat2 in zip(features1, features2):
        cos_similarity = np.dot(feat1, feat2) / (np.linalg.norm(feat1) * np.linalg.norm(feat2))
        similarities.append(cos_similarity)

    avg_similarity = np.mean(similarities)
    return avg_similarity > threshold, avg_similarity
