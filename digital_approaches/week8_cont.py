# Yue "Cherry" Ying
# Python Exercise for Tuesday March 2nd

import os
import re
import sys
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
import numpy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, Text, tokenize
import joblib as joblib
from joblib import dump, load
import csv
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split


countvectorizer = joblib.load('CountVectorizerModel.joblib')
lda = joblib.load('LDAModel.joblib')

def preprocess_text(text, stopwords, lemmatizer):
    tokens = re.findall(r"\w+", text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    tokens = [token for token in tokens if token not in stopwords]
    return " ".join(tokens)

if __name__ == "__main__":
    folders = ["talk.politics.mideast", "rec.autos", "comp.sys.mac.hardware", "alt.atheism", 
    "comp.os.ms-windows.misc", "rec.sport.hockey", "sci.crypt", "sci.med", "talk.politics.misc", 
    "rec.motorcycles", "comp.windows.x", "comp.graphics", "comp.sys.ibm.pc.hardware", "sci.electronics",
    "talk.politics.guns", "sci.space", "soc.religion.christian", "misc.forsale", "talk.religion.misc"]
    
    texts = []
    categories = []
    stopwords = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    for category in folders:
        for file in os.scandir("../20news/" + category):
            with open(file.path, encoding="latin-1") as input_file: # texts have latin-1 encoding
                text = input_file.read()
            text = preprocess_text(text, stopwords, lemmatizer)
            texts.append(text)
            categories.append(category)
    vectorizer = countvectorizer
    vectorized_texts = vectorizer.fit_transform(texts)
    doc_topic_distrib = lda.fit_transform(vectorized_texts)
    with open("news_topic_dist.csv", 'w') as news:
        print(doc_topic_distrib, file=news)
