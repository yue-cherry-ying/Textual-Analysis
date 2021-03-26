import sys
import os
import re
import numpy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from gensim.models import word2vec

def get_sentences(path_to_files):
    english_stopwords = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    tokenized_sentences = []
    with open(path_to_files) as f:
        text = f.read()
        text = re.sub(r"<[^>]+>", "", text) # remove all tags
        text = re.sub(r"\dth", "", text)
        text = re.sub(r"_\w+_", "", text)
        text = re.sub(r"\w+_", "", text)
        text = re.sub(r"_\w+", "", text)
    sentences = re.split(r"[!?.]+", text)
    for sentence in sentences:
        sentence = sentence.lower()
        sentence = re.findall(r"\w+", text)
        sentence = [lemmatizer.lemmatize(token).lower() for token in sentence if token not in english_stopwords]
        sentence = [token for token in sentence if not token.isdigit()]
        tokenized_sentences.append(sentence)
    return tokenized_sentences


if __name__ == "__main__":
    path = sys.argv[1]
    window_size = int(sys.argv[2])

    print("Getting sentences...")
    path = sys.argv[1]
    sentences = get_sentences(path)

    print("Training model...")
    model = word2vec.Word2Vec(sentences, min_count=10, window=window_size)

    while True:
        word = input("\nType word: ")
        print(f"Most similar words to {word}:")
        for word, score in model.wv.most_similar(word):
            print(f"{word}: {score}")