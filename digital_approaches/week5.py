# Yue "Cherry" Ying
# Python Exercise for Tuesday Feb. 7th

import re
from nltk import Text, tokenize, FreqDist, pos_tag
from nltk.corpus import stopwords

frankenstein_text = ""
in_the_text = False
with open("../texts/frankenstein.txt") as text:
    for line in text:
        if re.search(r"Letter 1\n", line):
            in_the_text = True
        if in_the_text:
            frankenstein_text += line

frankenstein_tokens = tokenize.word_tokenize(frankenstein_text)
frankenstein = Text(frankenstein_tokens)
is_noun = lambda pos: pos[:2] == 'NN' # function to test if somthing is a noun
frankenstein_pos = pos_tag(frankenstein, tagset="universal")  # => returns a list of tuples
frankenstein_nouns = [word for (word, pos) in pos_tag(frankenstein) if is_noun(pos)] # extract all nouns from Frankenstein
# print(frankenstein_nouns)

frankenstein_filtered_tokens = []
english_stopwords = stopwords.words("english")
for word, pos in frankenstein_pos:
    word = word.lower()
    if pos == "NOUN" and word not in english_stopwords and re.search(r"\w", word):
        frankenstein_filtered_tokens.append(word)
frankenstein_filtered_tokens_freq_dist = FreqDist(frankenstein_filtered_tokens) # most common nouns for Frankeinstein
# print(frankenstein_filtered_tokens_freq_dist.most_common(50))

dracula_text = ""
in_the_text = False
with open("../texts/dracula.txt") as text:
    for line in text:
        if re.search(r"CHAPTER I\n", line):
            in_the_text = True
        if in_the_text:
            if re.search(r"\nPage", line):
                in_the_text = False
            dracula_text += line

dracula_tokens = tokenize.word_tokenize(dracula_text)
dracula = Text(dracula_tokens)
is_noun = lambda pos: pos[:2] == 'NN' # function to test if somthing is a noun
dracula_pos = pos_tag(dracula, tagset="universal")  # => returns a list of tuples
dracula_nouns = [word for (word, pos) in pos_tag(dracula) if is_noun(pos)] # extract all nouns from Dracula
# print(dracula_nouns)

dracula_filtered_tokens = []
english_stopwords = stopwords.words("english")
for word, pos in dracula_pos:
    word = word.lower()
    if pos == "NOUN" and word not in english_stopwords and re.search(r"\w", word):
        dracula_filtered_tokens.append(word)
dracula_filtered_tokens_freq_dist = FreqDist(dracula_filtered_tokens) # most common nouns for Dracula
# print(dracula_filtered_tokens_freq_dist.most_common(50))

frankenstein_noun_list = frankenstein_filtered_tokens_freq_dist.most_common(100)
dracula_noun_list = dracula_filtered_tokens_freq_dist.most_common(100)

freq_noun_frankenstein_not_dracula = []
freq_noun_dracula_not_frankenstein = []
for frankenstein_word in frankenstein_noun_list:
    for dracula_word in dracula_noun_list:
        if frankenstein_word[0] != dracula_word[0]:
            if frankenstein_word not in freq_noun_frankenstein_not_dracula:
                freq_noun_frankenstein_not_dracula.append(frankenstein_word)
            if dracula_word not in freq_noun_dracula_not_frankenstein:
                freq_noun_dracula_not_frankenstein.append(dracula_word)
twenty_frankenstein = freq_noun_frankenstein_not_dracula[:20] # 20 most frequent nouns for Frankenstein that don't occur in Dracula
twenty_dracula = freq_noun_dracula_not_frankenstein[:20] # 20 most frequent nouns for Dracula that don't occur in Frankenstein
# print(twenty_frankenstein)
# print(twenty_dracula)