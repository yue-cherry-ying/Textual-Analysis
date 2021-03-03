#!/usr/bin/env python3

import sys
import os
import re
import numpy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, Text, tokenize
from nltk.collocations import BigramCollocationFinder
from nltk.metrics import BigramAssocMeasures


def get_federalist_author_text(path_to_files):
    authors = {}
    english_stopwords = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    for author in os.scandir(path_to_files):
        authors[author.name] = []
        for file in os.scandir(author.path):
            with open(file.path) as input_file:
                text = input_file.read()
                text = re.sub(r"<[^>]+>", "", text)
            tokens = re.findall(r"\w+", text)
            filtered_tokens = [
                lemmatizer.lemmatize(token).lower() for token in tokens if token not in english_stopwords
            ]
            authors[author.name].extend(filtered_tokens)
    return authors


if __name__ == "__main__":
    path = sys.argv[1]
    window_size = int(sys.argv[2])

    authors = get_federalist_author_text(path)
    authors_bcf = {}
    for author, words in authors.items():
        print(f"Building co-occurrence representation for {author}...")
        bcf = BigramCollocationFinder.from_words(words, window_size=window_size)
        authors_bcf[author] = bcf

    while True:
        word = input("Type a word to get top 5 associated words for each author (CTRL+C to quit): ")
        for author, bcf in authors_bcf.items():
            likelihood_scores = []

            for target_word in bcf.word_fd:
                likelihood_score = bcf.score_ngram(BigramAssocMeasures.likelihood_ratio, word, target_word)
                likelihood_scores.append((target_word, likelihood_score or 0))

            print(f"\n### Top 10 associated words as measured by Log-likelihood score for {author} ###")
            for target_word, score in sorted(likelihood_scores, key=lambda x: x[1], reverse=True)[:10]:
                print(f"{target_word}: {score}")
