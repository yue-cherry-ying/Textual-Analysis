from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import os
import csv

def preprocess_text(text, stopwords, lemmatizer):
    tokens = re.findall(r"\w+", text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    tokens = [token for token in tokens if token not in stopwords]
    return " ".join(tokens)

if __name__ == "__main__":
    sentences = []
    labels = []
    stopwords = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    for file in os.scandir("../sentiment_labelled_sentences"):
        with open(file.path) as input_file:
            for line in input_file:
                line = line.strip()
                sentence, label = line.split("\t") # split the line, returns 2 items
                sentences.append(preprocess_text(sentence, stopwords, lemmatizer))
                labels.append(label)
    vectorizer = TfidfVectorizer()
    vectorized_text = vectorizer.fit_transform(sentences)
    new_texts = []
    with open("tweets.csv") as csv_file:
        csv_reader = csv.DictReader(csv_file) # the DictReader reads the file automatically label the columns for you
        for row in csv_reader:
            new_texts.append(preprocess_text(row["text"], stopwords, lemmatizer))
    vectorized_tweets = vectorizer.transform(new_texts)
    classifier = MultinomialNB()
    classifier.fit(vectorized_text, labels)
    predicted_classes = classifier.predict(vectorized_tweets)
    with open("tweets_classified.txt", 'w') as tweets:
        for doc, category in zip(new_texts, predicted_classes):
            print(doc, category, file=tweets)

    reviews = []
    with open("amazon_alexa.tsv") as csv_file:
        csv_reader = csv.DictReader(csv_file, delimiter="\t") # the DictReader reads the file automatically label the columns for you
        for row in csv_reader:
            reviews.append(preprocess_text(row["verified_reviews"], stopwords, lemmatizer))
    reviews_vectorized = vectorizer.transform(reviews)
    classifier = MultinomialNB()
    classifier.fit(vectorized_text, labels)
    predicted_classes = classifier.predict(reviews_vectorized)
    with open("amazon_classified.txt", 'w') as reviews:
        for doc, category in zip(reviews, predicted_classes):
            print(doc, category, file=reviews)