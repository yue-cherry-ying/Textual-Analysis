#!/usr/bin/env python3

from joblib import load
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import sys


def get_closest(word, vectors, index_to_word, word_to_index):
    word_index = word_to_index[word]
    word_vector = vectors[word_index:word_index+1]
    result_vector = cosine_similarity(word_vector, vectors)
    ordered_word_indexes = np.argsort(result_vector)[0][::-1][1:11]
    results = [(index_to_word[index], result_vector[0, index]) for index in ordered_word_indexes]
    return results

if __name__ == "__main__":
    word_vector_model = load(sys.argv[1])
    vectors = word_vector_model["embeddings"]
    index_to_word = word_vector_model["feature_names"]
    word_to_index = {value: key for key, value in enumerate(index_to_word)}
    while True:
        word = input("\nType a word to find most associated words in trained corpus: ")
        results = get_closest(word, vectors, index_to_word, word_to_index)
        print(f"\n10 most associated words with {word}:")
        for term, score in results:
            print(term, score)