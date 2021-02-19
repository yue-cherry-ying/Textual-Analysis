#!/usr/bin/env python3

import re
from collections import Counter # returns a dictionary with counts
from nltk import tokenize, Text, pos_tag
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer # special database for lemmatizers

def get_noun_count(filename):
    text = ""
    in_the_text = False
    with open(filename) as doc:
        for line in doc:
            if "JONATHAN HARKER'S JOURNAL" in line or "Letter 1" in line: # filter both texts at the same time (can do this in one line since the chapters layouts are different)
                in_the_text = True
            if in_the_text:
                text += line
    text_tokens = tokenize.word_tokenize(text)
    nltk_text = Text(text_tokens)
    english_stopwords = stopwords.words("english")
    lemmatizer = WordNetLemmatizer() # initialize lemmatizer
    nouns = []
    for word, pos in pos_tag(nltk_text): # universal tagset returns readable tags such as "NOUN", the default uses tags such as "NN"
        word = word.replace("-", "")
        if not re.search(r"\W", word) and word not in english_stopwords and pos == "NN" or pos == "NNS": # "NNS" refers to plural nouns # the re.search is matching - non-word characters
            word = word.lower()
            lemma = lemmatizer.lemmatize(word)
            # if pos == "NNS":
            #     print(word, lemmatizer.lemmatize(word))
            #     exit() # this will return the lemmatized version of the plural word (singular version)
            nouns.append(word) # a list of nouns
    noun_count = Counter(nouns) # counter is a wrapper around the dictionary, so we can use .items()
    noun_count = dict(sorted(noun_count.items(), key=lambda x:x[1], reverse=True))
    # noun_set = {noun for noun, count in noun_count} # if you convert it to a set, then it will not have the values, it will be a string of all the keys, and then you can also call if something in the set.
    return noun_count # the function returns noun counts for any text -> type: dictionary

dracula = get_noun_count("../texts/dracula.txt")
frankenskein = get_noun_count("../texts/frankenstein.txt")
dracula_specific = [noun for noun in dracula if noun not in frankenskein][:20] # you can check if something is in or not in a dictionary, like how you do it in a list
frankenstein_specific = [noun for noun in frankenskein if noun not in dracula][:20]
print(f"DRACULA: {' '.join(dracula_specific)}")
print(f"FRANKENSTEIN: {' '.join(frankenstein_specific)}")