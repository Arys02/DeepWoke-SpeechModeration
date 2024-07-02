import numpy as np


def text_to_vector(text, ft):
    words = text.split(' ')
    word_vectors = [ft.get_word_vector(word) for word in words if word in ft.words]
    if not word_vectors:
        return np.zeros(300)
    return np.mean(word_vectors, axis=0)
