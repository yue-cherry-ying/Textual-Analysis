# !/usr/bin/env python3

import re

current_character = ""
character_list = []
in_character_tag = False
current_paragraph = ""
paragraphs = []
in_paragraph_tag = False
in_body = False

# Counting paragraphs per chapter in DRC
with open("../pride_and_prejudice.xml") as input_file:
    for line in input_file:
        line = line.strip()
        if '''<title type="main">''' in line:
            # title = re.sub(r"</?[^>]+>", "", line) # solution 1: replace <tag> with nothing
            title = re.sub(r"[^>]+>([^<]+).*", r"\1", line) # solution 2: match the entire line, get the text of the title
        if "<author>" in line:
            author = re.sub(r"[^>]+>([^<]+).*", r"\1", line)
        if "<date>" in line:
            date = re.sub(r"[^>]+>([^<]+).*", r"\1", line)
        if "<persName" in line:
            in_character_tag = True
            current_character = line # this captures situation when <persName> tag is in the same line of the content we want to extract
        if "</persName" in line:
            # Method 1:
            # current_character = re.sub(r"</?[^>]+>", " ", current_character) # substituting the tags with an empty space
            # current_character = re.sub(r"\s{2}", " ", current_character) # if there are 2 spaces, replace it with 1 space
            # Method 2:
            current_character = re.findall(r">([^>]+)<", current_character) # the findall method would only find what's in the ()
            current_character = " ".join(current_character) # concatenate the string items in a list => join elements from a list separated by a space
            in_character_tag = False
            character_list.append(current_character)
            current_character = "" # reset the current character so that we can capture the next character in the text
        if in_character_tag:
            current_character += line
        if "<body>" in line:
            in_body = True
        if in_body:
            if "<p>" in line:
                current_paragraph = line
                in_paragraph_tag = True
            elif "</p>" in line:
                current_paragraph += line # add the </p>, but not necessary since we will get rid of all tags in the end
                current_paragraph = re.sub(r"</?[^>]+>", "", current_paragraph)
                in_paragraph_tag = False
                paragraphs.append(current_paragraph)
            if in_paragraph_tag: # want to make sure adding paragraph text only happens when we are in the paragraph tag
                current_paragraph += line 
# print("\n\n".join(paragraphs))
# print(paragraphs[0]) # first paragraph of the text
# print(paragraphs[-1]) # last paragraph of the text