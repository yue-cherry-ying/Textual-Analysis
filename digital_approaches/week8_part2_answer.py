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


vectorizer = joblib.load('CountVectorizerModel.joblib')
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
    additional_stopwords = {"quot", "one", "two", "would", "new", "may", "he", "it", "told"} # add additional stopwords
    stopwords.update(additional_stopwords)
    lemmatizer = WordNetLemmatizer()
    # print("Processing texts", end=" ", flush=True)
    for category in folders:
        for file in os.scandir("../20news/" + category):
            with open(file.path, encoding="latin-1") as input_file: # texts have latin-1 encoding
                text = input_file.read()
            tokens = tokenize.word_tokenize(text)
            text_object = Text(tokens)
            text_with_pos = pos_tag(text_object, tagset="universal")
            filtered_tokens = [word for word, pos in text_with_pos if pos == "NOUN"]
            tokens = [lemmatizer.lemmatize(token) for token in filtered_tokens]
            tokens = [token for token in tokens if token not in stopwords]
            text = " ".join(tokens)
            texts.append((file.name, text))
            print(".", end="", flush=True)
        break

    vectorized_texts = vectorizer.transform([t[1] for t in texts])
    doc_topic_distrib = lda.transform(vectorized_texts)
    print("done.")

    print("\nStoring results...")
    with open("20news.lda.topic_distribution.csv", 'w') as csv_output:
        csvwriter = csv.writer(csv_output)
        csvwriter.writerow(["Filename", "Topic 1", "Topic 2", "Topic 3"])
        for doc, topics in enumerate(doc_topic_distrib):
            doc_name = texts[doc][0]
            topic_values = []
            top_topic_weight_indices = numpy.argsort(topics)[::-1][:3]
            for topic in top_topic_weight_indices:
                topic_weight = round(topics[topic], 3)
                topic_value = f"{topic} ({topic_weight})"
                topic_values.append(topic_value)
            row = [doc_name, topic_values[0], topic_values[1], topic_values[2]]
            csvwriter.writerow(row)