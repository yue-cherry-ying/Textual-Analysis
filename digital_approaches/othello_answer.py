# !/usr/bin/env python 3

# The structure of the text file:
# 1. New lines between the "ACT" and the speech
# 2. All capital letters for character name
# 3. Brackets

import re

# Generally speaking, it is advisable to read the file line by line
#  In this file, particular, we know it's structured line by line

# characters = set() # in Python, you get unique elements in a set
characters = {}
current_character = ""
with open("othello.txt") as input_file:
    for line in input_file:
        line = line.strip()
        # re.match only matches the beginning of a line (in this case, it's approriate to use re.match because our character names are at the beginning of the line)
        # re.search matches everything in a line
        if re.match(r"[A-Z]+$", line):
            current_character = line
            if current_character not in characters:
                characters[current_character] = [] # define an empty list for each character
            # print(repr(line)) # print the representation of a line
            continue 
        elif current_character == "":
            continue
        words = re.findall(r"\w+", line) # match words
        characters[current_character] += words
character_word_count = sorted(characters.items(), key=lambda x: len(x[1]), reverse=True) # len(x[1]) => sort by the value instead of the key, and sort by the length of the value
with open("character_word_counts", "w") as output_file:
    for character, words in character_word_count:
        # output_file.write(character)
        # output_file.write(" ")
        # output_file.write(str(len(words)))
        # output_file.write("\n")
        print(character, str(len(words)), file=output_file) # if you want to add a new line in between each output, then use print statement is easier/quicker

all_words = {}
for words in characters.values():
    for word in words:
        word = word.lower()
        if word not in all_words:
            all_words[word] = 0
        all_words[word] += 1 # get all words in the file, in lowercase
all_words_sorted = sorted(all_words.items(), key=lambda x: x[1], reverse=True)
most_frequent_words = all_words_sorted[:100]

word_filter = set(dict(most_frequent_words).keys())

character_words_counted = {}
for character, words in characters.items():
    words_filtered = {}
    for word in words:
        word = word.lower()
        if word not in word_filter:
            words_filtered[word] = 0
        words_filtered[word] += 1
    words_filtered_sorted = sorted(words_filtered.items(), key=lambda x:x[1], reverse=True)
    with open(character, "w") as output_file:
        for word, word_count in words_filtered_sorted[:20]:
            print(word, word_count, file=output_file)
            
# Notes:
# 1. Regular Expression
# use raw string in regular expression re.match(r" ")
# ^ => beginning of the string (needed if you use re.search() method)
# $ => the end of a string
# if we want to match 2 or more instances, use r"[A-Z]{2,}"

# 2. Addition in a set
# characters.add(line)
