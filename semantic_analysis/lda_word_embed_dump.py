import csv
import os
import re
import sys

import joblib
import numpy
from nltk import Text, pos_tag, tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer


def get_reuters_files(path_to_files):
    """Get content of Reuters files"""
    docs = []
    english_stopwords = set(stopwords.words("english"))
    additional_stopwords = {"quot", "one", "two", "would", "new", "may", "he", "it", "told"}
    english_stopwords.update(additional_stopwords)
    lemmatizer = WordNetLemmatizer()
    for file in os.scandir(path_to_files):
        with open(file.path) as input_file:
            text = input_file.read()
            text = re.sub(r"<[^>]+>", "", text)
        tokens = tokenize.word_tokenize(text)
        text_object = Text(tokens)
        text_with_pos = pos_tag(text_object, tagset="universal")
        filtered_tokens = [word for word, pos in text_with_pos if pos == "NOUN"]
        filtered_tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens if token not in english_stopwords]
        docs.append((file.name, " ".join(filtered_tokens)))
    return docs


if __name__ == "__main__":
    path_to_files = sys.argv[1]
    print("Reading files...", end=" ", flush=True)
    text_files = get_reuters_files(path_to_files)
    print("done.")

    print("Vectorizing texts...", end=" ", flush=True)
    vectorizer = CountVectorizer(max_df=0.9, min_df=0.005)  # LDA works with CountVectorizer (no TF-IDF weighting)
    vectorized_data = vectorizer.fit_transform((doc[1] for doc in text_files))
    print("done.")

    print("Building LDA model using training set...", end=" ", flush=True)
    n_topics = int(sys.argv[2])
    lda = LatentDirichletAllocation(n_components=n_topics)
    doc_topic_distrib = lda.fit_transform(vectorized_data)  # learns model and return document-topic matrix
    print("done.")

    print("\nStoring results...")
    feature_names = vectorizer.get_feature_names()
        
    word_topic_matrix = lda.components_.transpose()
    word_model = {"feature_names": feature_names, "embeddings": word_topic_matrix}
    joblib.dump(word_model, f"word_embeddings_lda_{n_topics}.model")
