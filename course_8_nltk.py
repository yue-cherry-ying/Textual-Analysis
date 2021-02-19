#!/usr/bin/env python3

import re
from nltk import Text, tokenize, FreqDist, pos_tag
from nltk.corpus import stopwords

great_expectations_text = ""
in_the_text = False
with open("texts/great_expectations.txt") as text:
    for line in text:
        if re.search(r"Chapter I\n", line):
            in_the_text = True
        if in_the_text:
            great_expectations_text += line

great_expectations_tokens = tokenize.word_tokenize(great_expectations_text)  # => equivalent of re.split(r"(\W+)", str)
great_expectations = Text(great_expectations_tokens)  # => load text into NLTK for analysis

# Get concordances
# great_expectations.concordance("home", lines=10)

# Get words used in a similar context
# great_expectations.similar("gentleman", 10)

# Get the most common tokens (includes punctuation)
# freq_dist_great_expectations = FreqDist(great_expectations)
# most_common_tokens = freq_dist_great_expectations.most_common(50)

# Get the most common words
# clean_tokens = re.findall(r"\w+", great_expectations_text)
# freq_dist_great_expectations = FreqDist(clean_tokens)
# print(freq_dist_great_expectations.most_common(50))

# Import prebuilt English stopword list
# english_stopwords = stopwords.words("english")
# print(english_stopwords)

# Filter out common function words
# clean_tokens = re.findall(r"\w+", great_expectations_text)
# filtered_tokens = []
# for token in clean_tokens:
#     token = token.lower()
#     if token in english_stopwords:
#         continue
#     filtered_tokens.append(token)
# filtered_tokens_freq_dist = FreqDist(filtered_tokens)
# print(filtered_tokens_freq_dist.most_common(50))

# Identify part-of-speech
# great_expectations_pos = pos_tag(great_expectations, tagset="universal")  # => returns a list of tuples
# print(great_expectations_pos[:40])

# Get a frequency distribution of most common nouns
# filtered_tokens = []
# for word, pos in great_expectations_pos:
#     word = word.lower()
#     if pos == "NOUN" and word not in english_stopwords and re.search(r"\w", word):
#         filtered_tokens.append(word)
# filtered_tokens_freq_dist = FreqDist(filtered_tokens)
# print(filtered_tokens_freq_dist.most_common(50))

# Get most common collocates
# filtered_text = Text(filtered_tokens)
# filtered_text.collocations()

