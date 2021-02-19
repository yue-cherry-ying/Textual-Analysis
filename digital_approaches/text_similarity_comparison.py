#!/usr/bin/env python3

from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import re
import numpy

def read_and_tokenize_doc(filename, stopwords):
    with open(filename) as text:
        text_contents = text.read()
    tokens = re.findall(r"\w+", text_contents)
    filtered_tokens = []
    for token in tokens:
        if token not in english_stopwords and re.search(r"[!,?;.:]", token) is None:
            filtered_tokens.append(token)
    filtered_text = " ".join(filtered_tokens)
    return filtered_text

if __name__ == "__main__":
    english_stopwords = set(stopwords.words("english")) # the set allows us to reduce the runtime
    documents = [
        ("Dracula", "../texts/dracula.txt"),
        ("Frankenstein", "../texts/frankenstein.txt"),
        ("Great Expectations", "../texts/great_expectations.txt"),
        ("Pride and Prejudice", "../texts/pride_and_prejudice.txt")
    ]
    clean_docs = [read_and_tokenize_doc(doc[1], english_stopwords) for doc in documents] # tokenize into strings, without the title of the texts, but since we did a for loop, each location correspond to the right text
    vectorizer = TfidfVectorizer(min_df=2) # to make sure that a word occurs in at least 2 documents -> this is to make sure that we are not comparing similarity between unique words in a specific text (ex. character names)
    corpus_vectorized = vectorizer.fit_transform(clean_docs)
    results = cosine_similarity(corpus_vectorized) # the most common method to find the similarity between texts is cosine_similarity
    # the result matrix is another matrix, each row is a document, and each column is another document for which it compares similarity to
    # the first row corresponds to the first document (there are 4 texts, thus the matrix is 4 by 4)
    print(corpus_vectorized.shape, results.shape) # the second number in corpus_vectorized shape is the number of words in a corpus
    for doc_pos, result_vector in enumerate(results): # doc_pos refers to each row
        outer_doc_name = documents[doc_pos][0]
        results = {}
        for doc_index, score in enumerate(result_vector): # result_vector is the similarity between texts (1 by 4 matrix for each row)
            inner_doc_name = documents[doc_index][0] # doc_index refers to each column
            if inner_doc_name != outer_doc_name:
                results[inner_doc_name] = score
        doc, score = sorted(results.items(), key=lambda x: x[1], reverse=True)[0]
        print(outer_doc_name, doc, score)
            # for inner_doc, score in sorted(results.items(), key=lambda x: x[1], reverse=True)[:1]:
            #     print(outer_doc_name, inner_doc, score)
            #     print(f"{outer_doc_name}-{inner_doc_name}: {score}")