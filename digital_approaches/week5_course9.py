# Yue "Cherry" Ying
# Python Exercise for Thursday Feb. 11th

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from nltk import word_tokenize
import numpy
import re

def tokenize_text(file, english_stopwords):
    with open(file) as text:
        text_contents = text.read()
    tokens = re.findall(r"\w+", text_contents)
    filtered_tokens = []
    for token in tokens:
        if token not in english_stopwords and re.search(r"[!,?;.:]", token) is None:
            filtered_tokens.append(token)
    filtered_text = " ".join(filtered_tokens)
    return filtered_text

if __name__ == '__main__':
    english_stopwords = set(stopwords.words('english'))
    expectations = tokenize_text("../texts/great_expectations.txt", english_stopwords)
    pride = tokenize_text("../texts/pride_and_prejudice.txt", english_stopwords)
    frankenstein = tokenize_text("../texts/frankenstein.txt", english_stopwords)
    dracula = tokenize_text("../texts/dracula.txt", english_stopwords)
    documents = [expectations, pride, frankenstein, dracula]
    vectorizer = TfidfVectorizer()
    corpus_vectorized = vectorizer.fit_transform(documents)
    sorted_indices = numpy.argsort(vectorizer.idf_)[::-1]
    features = vectorizer.get_feature_names()
    # print([features[i] for i in sorted_indices]) # most similar texts among 4 texts

    # expectation vs. pride
    expectation_pride = [expectations, pride]
    vectorizer1 = TfidfVectorizer()
    expectation_pride_vectorized = vectorizer1.fit_transform(expectation_pride)
    sorted_indices1 = numpy.argsort(vectorizer1.idf_)[::-1]
    features1 = vectorizer1.get_feature_names()
    # print([features1[i] for i in sorted_indices1]) # most similar texts between "Great Expectation" and "Pride and Prejudice"

    # expectation vs. frankenstein
    expectation_frankenstein = [expectations, frankenstein]
    vectorizer2 = TfidfVectorizer()
    expectation_frankenstein_vectorized = vectorizer2.fit_transform(expectation_frankenstein)
    sorted_indices2 = numpy.argsort(vectorizer2.idf_)[::-1]
    features2 = vectorizer2.get_feature_names()
    # print([features2[i] for i in sorted_indices2]) # most similar texts between "Great Expectation" and "Frankenstein"
    
    # expectation vs. dracula
    expectation_dracula = [expectations, dracula]
    vectorizer3 = TfidfVectorizer()
    expectation_dracula_vectorized = vectorizer3.fit_transform(expectation_dracula)
    sorted_indices3 = numpy.argsort(vectorizer3.idf_)[::-1]
    features3 = vectorizer3.get_feature_names()
    # print([features3[i] for i in sorted_indices3]) # most similar texts between "Great Expectation" and "Dracula"

    # pride vs. frankenstein
    pride_frankenstein = [pride, frankenstein]
    vectorizer4 = TfidfVectorizer()
    pride_frankenstein_vectorized = vectorizer4.fit_transform(pride_frankenstein)
    sorted_indices4 = numpy.argsort(vectorizer4.idf_)[::-1]
    features4 = vectorizer4.get_feature_names()
    # print([features4[i] for i in sorted_indices4]) # most similar texts between "Pride and Prejudice" and "Frankenstein"

    # pride vs. dracula
    pride_dracula = [pride, dracula]
    vectorizer5 = TfidfVectorizer()
    pride_dracula_vectorized = vectorizer5.fit_transform(pride_dracula)
    sorted_indices5 = numpy.argsort(vectorizer5.idf_)[::-1]
    features5 = vectorizer5.get_feature_names()
    # print([features5[i] for i in sorted_indices5]) # most similar texts between "Pride and Prejudice" and "Dracula"

    # frankenstein vs. dracula
    frankenstein_dracula = [frankenstein, dracula]
    vectorizer6 = TfidfVectorizer()
    frankenstein_dracula_vectorized = vectorizer6.fit_transform(frankenstein_dracula)
    sorted_indices6 = numpy.argsort(vectorizer6.idf_)[::-1]
    features6 = vectorizer6.get_feature_names()
    # print([features6[i] for i in sorted_indices6]) # most similar texts between "Frankenstein" and "Dracula"