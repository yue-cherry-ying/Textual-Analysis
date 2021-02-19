import re
from nltk import Text, tokenize, FreqDist, pos_tag, ne_chunk
from nltk.corpus import stopwords

# Book I Analysis

DRC_text = ""
in_the_text = False
with open("DRC_BookI.txt") as text:
    for line in text:
        if re.search(r"CHAPTER I.\n", line):
            in_the_text = True
        if in_the_text:
            DRC_text += line

DRC_tokens = tokenize.word_tokenize(DRC_text)  # => equivalent of re.split(r"(\W+)", str)
DRC = Text(DRC_tokens)  # => load text into NLTK for analysis

# https://www.programcreek.com/python/example/91258/nltk.ne_chunk


# Get concordances
# DRC.concordance("pao-yu", lines=10)

# Get words used in a similar context
# DRC.similar("gentleman", 10)
# DRC.similar("lady", 10)
# DRC.similar("maid", 10)
# DRC.similar("mansion", 10)
# DRC.similar("wife", 10)
# DRC.similar("chia", 10)
# DRC.similar("hsueh", 10)

# Get the most common tokens (includes punctuation)
# freq_dist_DRC = FreqDist(DRC)
# most_common_tokens = freq_dist_DRC.most_common(50)
# print(most_common_tokens)

# Get the most common words
# clean_tokens = re.findall(r"\w+", DRC_text)
# freq_dist_DRC = FreqDist(clean_tokens)
# print(freq_dist_DRC.most_common(50))

# Import prebuilt English stopword list
# english_stopwords = stopwords.words("english")
# print(english_stopwords)

# Filter out common function words
# clean_tokens = re.findall(r"\w+", DRC_text)
# filtered_tokens = []
# for token in clean_tokens:
#     token = token.lower()
#     if token in english_stopwords:
#         continue
#     filtered_tokens.append(token)
# filtered_tokens_freq_dist = FreqDist(filtered_tokens)
# print(filtered_tokens_freq_dist.most_common(50))

# Identify part-of-speech
# DRC_pos = pos_tag(DRC, tagset="universal")  # => returns a list of tuples
# print(DRC_pos[:40])

# Get a frequency distribution of most common nouns
# filtered_tokens = []
# for word, pos in DRC_pos:
#     word = word.lower()
#     if pos == "NOUN" and word not in english_stopwords and re.search(r"\w", word):
#         filtered_tokens.append(word)
# filtered_tokens_freq_dist = FreqDist(filtered_tokens)
# print(filtered_tokens_freq_dist.most_common(50))

# Get most common collocates
# filtered_text = Text(filtered_tokens)
# filtered_text.collocations()