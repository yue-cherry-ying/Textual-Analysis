import re

# Exercise 1: Parsing a TEI file using regular expressions:
characters = []
current_character = ""
author = ""
title = ""
date = ""
first_paragraph = ""
last_paragraph = ""
with open("pride_and_prejudice.xml") as input_file:
    for line in input_file:
        line = line.strip()
        if re.match(r"<author>", line):
            author = re.findall(r">.*<", line)
        if re.match(r"<title>", line):
            title = re.findall(r">.*<", line)
        if re.match(r"<date>", line):
            date = re.findall(r">.*<", line)
        if re.match(r"<forename>", line):
            current_character = re.findall(r">.*<", line)
            if current_character not in characters:
                characters.append(current_character)
            continue
        if current_character == "":
            continue
        if re.match(r"<p>", line):
            last_paragraph = re.findall(r">.*<", line)
            if first_paragraph == "":
                first_paragraph = re.findall(r">.*<", line)
            
     
# Exercise 2: Convert the pride_and_prejudice.txt file to TEI:
newtitle = ""     
newauthor = ""   
chapters = {}  
current_chapter = ""
with open("pride_and_prejudice.txt") as file:
    for line in file:
        line = line.strip()
        if re.match(r"Pride ", line):
            newtitle = re.findall(r".*", line)
        if re.match(r"Austen ", line):
            newauthor = re.findall(r".*", line)
        if re.match(r"Chapter.{1,}$", line):
            current_chapter = line
            if current_chapter not in chapters:
                chapters[current_chapter] = []
            continue
        if current_chapter == "":
            continue
        words = re.findall(r"\w+", line)
        chapters[current_chapter].extend(words)
            
         
with open("TEI", "w") as output_file:
    output_file.write('<?xml version="1.0" encoding="utf-8"?>')
    output_file.write("\n")
    output_file.write('<TEI>')
    output_file.write("\n")
    output_file.write('  <teiHeader>')
    output_file.write("\n")
    output_file.write('    <sourceDesc>')
    output_file.write("\n")
    output_file.write('      <titleStmt>')
    output_file.write("\n")
    output_file.write('        <title>' + str(newtitle) + '</title>')
    output_file.write("\n")
    output_file.write('        <author>' + str(newauthor) + '</author>')
    output_file.write("\n")
    output_file.write('      <titleStmt>')
    output_file.write("\n")
    output_file.write('    <sourceDesc>')
    output_file.write("\n")
    output_file.write('  <body>')
    output_file.write("\n")
    for chapter, words in chapters.items():
        print("<div>", chapter, str(words),"</div>", "\n", file=output_file)
    output_file.write("\n")
    output_file.write('  </body>')
    output_file.write("\n")
    output_file.write('  <teiHeader>')