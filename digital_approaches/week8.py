import os
import re
import sys
from sklearn.decomposition import LatentDirichletAllocation
from sklearn.feature_extraction.text import CountVectorizer
import numpy
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk import pos_tag, Text, tokenize

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