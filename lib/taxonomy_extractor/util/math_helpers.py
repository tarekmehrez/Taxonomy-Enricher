"""Contains the math helper functions."""
import numpy as np
from scipy.spatial.distance import cosine


def average_vectors(vectors):
    """
    Average given list of vectors.

    params:
        embedding (list[np.ndarray(float)])
    """
    return np.mean(vectors, axis=0)


def cosine_similarity(vector1, vector2):
    """
    Get cosing similarity between two vectors.

    params:
        vector1 (np.ndarray(float))
        vector2 (np.ndarray(float))
    """
    return cosine(vector1, vector2)
