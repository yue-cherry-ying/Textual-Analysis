# Yue "Cherry" Ying
# Python Exercise for Tuesday Feb. 23rd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import os
import pandas

def preprocess_text(filename, stopwords, lemmatizer):
    with open(filename) as text:
        for line in text:
            line = line.strip()
            tokens = re.findall(r"\w+", line)
            tokens = [lemmatizer.lemmatize(token) for token in tokens]
            full_tokens = [token for token in tokens if token not in stopwords]
            tokens = [token for token in tokens if token not in stopwords and re.search(r"\d", token) is None]
            filtered_text = " ".join(tokens)
            full_text = " ".join(full_tokens)
        return filtered_text, full_text

if __name__ == "__main__":
    texts = []
    full_texts = []
    categories = []
    english_stopwords = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    for file in os.scandir("../sentiment_labelled_sentences"):
        text, full_text = preprocess_text(file, english_stopwords, lemmatizer)
        texts.append(text)
        for line in full_text:
            if "1" in line:
                categories.append("positive")
            if "0" in line:
                categories.append("negative")
    vectorizer = TfidfVectorizer()
    vectorized_texts = vectorizer.fit_transform(texts)
    X_train, X_test, Y_train, Y_test = train_test_split(vectorized_texts, categories, test_size=0.25)
    classifier = MultinomialNB()
    classifier.fit(X_train, Y_train)
    accuracy = classifier.score(X_test, Y_test)
    # print(accuracy) # test accuracy of the model

    tweets_df = pandas.read_csv('../tweets.csv')
    tweets_doc_strings = tweets_df['text'].tolist()
    test_vectorized = vectorizer.transform(tweets_doc_strings)
    classifier.fit(vectorized_texts, categories)
    tweets_predicted_classes = classifier.predict(test_vectorized)
    # for doc, category in zip(tweets_doc_strings, tweets_predicted_classes):
    #     print(doc, category)
    with open("tweets_classification", "w") as output_file:
        for doc, category in zip(tweets_doc_strings, tweets_predicted_classes):
            print(doc, category, file=output_file)

    amazon_df = pandas.read_csv('../amazon_alexa.tsv', sep = '\t')
    amazon_doc_strings = amazon_df['verified_reviews'].tolist()
    test_vectorized = vectorizer.transform(amazon_doc_strings)
    classifier.fit(vectorized_texts, categories)
    amazon_predicted_classes = classifier.predict(test_vectorized)
    # for doc, category in zip(amazon_doc_strings, amazon_predicted_classes):
    #     print(doc, category)
    with open("amazon_classification", "w") as output_file:
        for doc, category in zip(amazon_doc_strings, amazon_predicted_classes):
            print(doc, category, file=output_file)
