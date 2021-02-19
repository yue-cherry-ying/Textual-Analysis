# Yue "Cherry" Ying
# Python Exercise for Tuesday January 26th

import re

# a) Counting words per characters in Othello
with open('othello.txt') as f:
    characters = []
    word_len = 0
    character_word = {}
    key = ""
    for line in f:
        words = line.split()
        character_word[key] = word_len
        if len(words) == 1:
            character = words[0]
            if re.match(r'\b[A-Z][A-Z]+\b', character):
                character_word[character] = character_word[key]
                key = character
        else:
            word_len += len(words)
            character_word[key] = word_len
    character_word.pop('')
    sort = sorted(character_word.items(), key=lambda x:x[1], reverse=True)
    outF = open("part_a.text", "w")
    for pair in sort:
        outF.write(str(pair))
        outF.write("\n")
    outF.close()

# b) Counting most frequent words per character
with open('othello.txt') as f:
    d = {}
    wordlist = []
    character_dict = {}
    key = ""
    for line in f:
        words = line.split()
        character_dict[key] = wordlist
        if len(words) == 1:
            character = words[0]
            if re.match(r'\b[A-Z][A-Z]+\b', character):
                character_dict[character] = wordlist
                key = character
        else:
            wordlist.append(words)
            character_dict[key] = wordlist
            wordlist = []
        for word in words:
            word = re.sub('[^\w\s]', '', word)
            if word in d:
                d[word] += 1
            else:
                d[word] = 1
    character_dict.pop('')
    freqword = sorted(d.items(), key=lambda x:x[1], reverse=True)
    hundredfreq = set(freqword[:100])
    # pair = {k: character_dict[k] for k in list(character_dict)[:1]}
    result = {}
    for key in character_dict:
        res = str([' '.join(ele) for ele in character_dict[key]]) 
        for text_word in res:
            for search_word in hundredfreq:
                if search_word == text_word:
                    res.replace('text_word','')
        result[key] = len(res)
    sort_result = sorted(result.items(), key=lambda x:x[1], reverse=True)
    outfile = open("part_b.text", "w")
    for p in sort_result:
        outfile.write(str(p))
        outfile.write("\n")
    outfile.close()



