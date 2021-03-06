# Yue "Cherry" Ying
# Python Exercise for Tuesday March 2nd

import os
import re
import sys
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import numpy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, Text, tokenize
import joblib as joblib
from joblib import dump, load
import csv

def get_reuters_files(path_to_files):
    """Get content of Reuters files"""
    docs = []
    english_stopwords = set(stopwords.words("english"))
    additional_stopwords = {"quot", "one", "two", "would", "new", "may", "he", "it", "told"} # add additional stopwords
    english_stopwords.update(additional_stopwords)
    lemmatizer = WordNetLemmatizer()
    for file in os.scandir(path_to_files):
        with open(file.path) as input_file:
            text = input_file.read()
            text = re.sub(r"<[^>]+>", "", text) # remove all tags
        tokens = re.findall(r"\w+", text)
        filtered_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in english_stopwords]
        filtered_tokens = [word for word in filtered_tokens if not word.isdigit()] # filter out all digits
        docs.append((file.name, " ".join(filtered_tokens)))
    return docs

if __name__ == "__main__":
    path_to_files = sys.argv[1]
    print("Reading files...", end=" ", flush=True)
    # text_files = get_reuters_files("../reuters")
    text_files = get_reuters_files(path_to_files)
    print("done.")

    print("Vectorizing texts...", end=" ", flush=True)
    vectorizer = CountVectorizer(max_df=0.6) # LDA works with CountVectorizer (no TF-IDF weighting)
    vectorized_data = vectorizer.fit_transform((doc[1] for doc in text_files))
    joblib.dump(vectorizer, 'CountVectorizerModel.joblib')
    print("done.")

    print("Building LDA model using training set...", end=" ", flush=True)
    n_topics = int(sys.argv[2])
    # n_topics = 50
    lda = LatentDirichletAllocation(n_components=n_topics)
    doc_topic_distrib = lda.fit_transform(vectorized_data) # learns model and return document-topic matrix
    joblib.dump(lda, 'LDAModel.joblib')
    print("done.")

    # output to CSV for use in spreadsheet
    print("\nStoring results...")
    feature_names = vectorizer.get_feature_names()
    with open(f"{n_topics}.lda.topics.csv", "w") as csv_output:
        csvwriter = csv.writer(csv_output)
        csvwriter.writerow(["Label", "Topic Number", "Words"]) # Naming each column in our CSV file
        for topic_number, topic in enumerate(lda.components_): # lda.components_ contains the topic-word matrix
            # print(f"Topic #{topic_number}:", end=" ", file=output) # end=" " makes the output on the same line, not to the new line
            top_word_weight_indices = numpy.argsort(topic)[::-1][:20] # sort words in topic by weight and keep top 20
            words_in_topic = " ".join([feature_names[i] for i in top_word_weight_indices]) # map index value to word
            # print(words_in_topic, file=output_file)
            row = ["", topic_number, words_in_topic] # Emptu string for label
            csvwriter.writerow(row)

with open(f"{n_topics}.lda.topic_distribution.csv", "w") as csv_output:
    csvwriter = csv.writer(csv_output)
    csvwriter.writerow(["Filename", "Topic 1", "Topic 2", "Topic 3"]) # Naming each column in our CSV file
    for doc, topics in enumerate(doc_topic_distrib):
        doc_name = text_files[doc][0]
        topic_values = []
        top_topic_weight_indices = numpy.argsort(topics)[::-1][:5] # sort topics in doc by weight and keep top 5
        for topic in top_topic_weight_indices:
            topic_weight = topics[topic]
            topic_value = f"{topic} ({topic_weight})"
            topic_values.append(topic_value)
        # print(doc_name, ", ".join(topic_values), file=distribution)
        row = [doc_name, topic_values[0], topic_values[1], topic_values[2]]
        csvwriter.writerow(row)
