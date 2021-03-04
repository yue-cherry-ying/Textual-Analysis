#!/usr/bin/env python3

import sys
import os
import re
import numpy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.models import word2vec


def get_all_federalist_sentences(path_to_files):
    english_stopwords = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    tokenized_sentences_by_author = {} # a dictionary of authors as the keys and their sentences as values
    for author in os.scandir(path_to_files): # the author is the name of the folder
        if author.name in ("undertermined", "shared"):
            continue
        tokenized_sentences_by_author[author.name] = []
        for file in os.scandir(author.path):
            with open(file.path) as input_file:
                text = input_file.read()
                text = re.sub(r"<[^>]+>", "", text)
            sentences = re.split(r"[!?.]+", text)
            for sentence in sentences:
                sentence = sentence.lower()
                sentence = re.findall(r"\w+", text)
                sentence = [lemmatizer.lemmatize(token).lower() for token in sentence if token not in english_stopwords]
                tokenized_sentences_by_author[author.name].append(sentence)
    return tokenized_sentences_by_author


if __name__ == "__main__":
    path = sys.argv[1]
    window_size = int(sys.argv[2])

    print("Getting sentences...")
    path = sys.argv[1]
    sentences_by_author = get_all_federalist_sentences(path)
    model_per_author = {}

    # build a model for each author
    for author, sentences in sentences_by_author.items():
        print(f"Training model for {author}...")
        model = word2vec.Word2Vec(sentences, min_count=10, window=window_size) # if you have less data, try increasing the window size
        # model.save(f"{author}.model")
        model_per_author[author] = model

    while True:
        query_word = input("\nType word: ")
        for author, model in model_per_author.items():
            print(f"Most similar words to {query_word} in {author}:")
            for word, score in model.wv.most_similar(query_word):
                print(f"{word}: {score}")
