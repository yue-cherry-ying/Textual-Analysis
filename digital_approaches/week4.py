# Yue "Cherry" Ying
# Python Exercise for Tuesday Feb. 2nd

import re

# Exercise 1: Parsing a TEI file using regular expressions
title = ""
title_l = []
date_l = []
character = []
text = False
paragraph = False
text_content = []
with open("../pride_and_prejudice.xml") as input_file:
    for line in input_file:
        if text == True:
            text_content.append(line)
        # Extract the author, title, date from the file.
        if "<title" in line:
            t_pattern = r">([^<]+)"
            if re.search(t_pattern, line):
                title = re.search(t_pattern, line).groups()
                if title not in title_l:
                    title_l.append(title)
        elif "<author>" in line:
            a_pattern = r">([^<]+),"
            if re.search(a_pattern, line):
                author = re.search(a_pattern, line).groups()
        elif "<date>" in line:
            d_pattern = r">([^<]+)"
            if re.search(d_pattern, line):
                date = re.search(d_pattern, line).groups()
        # Extract the names of all characters of the novel: the names are \
        # defined inside the <listPerson> tag. For that, you will need to \
        # extract the text content of each <persName> tag contained in each \
        # <person> tag. 
        elif "<listPerson"  in line:
            continue
        elif "<persName>" in line:
            continue
        elif "<roleName"  in line:
            if re.search(r">([^<]+)", line):
                rolName = re.search(r">([^<]+)", line).groups()
        elif "<surname>" in line:
            if re.search(r">([^<]+)", line):
                surname = re.search(r">([^<]+)", line).groups()
                char_name = rolName[0]+" "+surname[0]
                if char_name not in character:
                    character.append(char_name)
        # Extract the contents of the first and last paragraphs
        elif "<text>" in line:
            text = True 
            text_content.append(line)
        elif "</text>" in line:
            text = False
    first_p = text_content[9].strip()
    fp = ''.join(re.findall(r">([^<]+)", first_p)) # Contents of the first paragraph

    last_p = text_content[-9].strip() + " " + \
        text_content[-8].strip() + " " + text_content[-7].strip()
    lp = ''.join(re.findall(r">([^<]+)", last_p)) # Contents of the last paragraph
    
    final_title = title_l[1][0] # Title of the book
    final_author = author[0] # Author of the book
    publication_date = date[0] # Publication Date of the Book
    
    for c in character:
        if "\n " in c:
            character.remove(c) # All characters of the novel (including their roles and surnames)
    # print(character)


# Exercise 2: Convert the pride_and_prejudice.txt file to TEI
with open('../teiHeader.txt', 'r') as f:
    prideTEI = open('week4_output.xml', 'w')
    for line in f:
        if "<author>" in line:
            line = "<author>Austen, Jane, 1775-1817</author>"
            prideTEI.write(line)
            prideTEI.write("\n")
        elif "<title>" in line:
            line = "<title>Pride and Prejudice</title>"
            prideTEI.write(line)
            prideTEI.write("\n")
        else:
            prideTEI.write(line)
    prideTEI.write("\n")
    prideTEI.write("<body>")
    with open('../pride_and_prejudice.txt', 'r') as text:
        chapter = False
        count = 0
        for line in text:
            if chapter == True:
                prideTEI.write(line)
                if line == "\n":
                    if (count % 2) == 0:
                        prideTEI.write("</p>")
                    else:
                        prideTEI.write("<p>")
                    count += 1
            elif "Chapter 1." in line:
                chapter = False
                prideTEI.write("<div1><head>")
                prideTEI.write(line)
                prideTEI.write("</head>")
                prideTEI.write("<p>")
                chapter = True
            elif ("Chapter" in line) and ("Chapter 1." not in line):
                chapter = False
                prideTEI.write("</div1>")
                prideTEI.write("<div1><head>")
                prideTEI.write(line)
                prideTEI.write("</head>")
                chapter = True
        prideTEI.write("\n")
        prideTEI.write("</body>")
        prideTEI.write("\n")
        prideTEI.write("</TEI>")
    prideTEI.close()