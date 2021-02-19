# !/usr/bin/env python3

import re
with open("pride_and_prejudice.tei", "w") as tei_file: # this creates a new file, if there is another file in the same system with the same name, then that file will be overwritten
    # print('<?xml version="1.0" encoding="utf-8"?>\n<TEI>', file=tei_file) # if the teiHeader does not have these lines
    with open("../teiHeader.txt") as input_file:
        for line in input_file:
            if "<author>" in line:
                line = line.replace("<author>", "<author>Austen, Jane")
            if "<title>" in line:
                line = line.replace("<title>", "<title>Pride and Prejudice")
            print(line, file=tei_file)
    with open("../pride_and_prejudice.txt") as input_file:
        in_the_text = False
        current_paragraph = ""
        for line in input_file:
            line = line.strip() # always do this first!
            if "Chapter 1." in line:
                in_the_text = True
                tag = "<body><div><head>" + line + "</head>"
                print(tag, file=tei_file)
                continue # if we see a chapter 1 tag, then we create a new div, but do not run the other lines
            if in_the_text:
                if "Chapter" in line:
                    tag = "</div><div><head>" + line + "</head>" # we close the previous chapter's </div>
                    print(tag, file=tei_file)
                    continue # if we see a chapter tag, then we create a new div, but do not run the other lines
                if re.search(r"w", line): # if there is character in the line
                    current_paragraph += line
                else:
                    if re.search(r"\w", current_paragraph):
                        current_paragraph = "<p>" + current_paragraph + "</p>"
                        print(current_paragraph, file=tei_file)
                        current_paragraph = ""
        print("</div></body></TEI>", file=tei_file)

