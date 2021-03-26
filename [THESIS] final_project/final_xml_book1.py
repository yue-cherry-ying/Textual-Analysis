import re

current_paragraph = ""
paragraphs = []
in_paragraph_tag = False
in_body = False
in_chapter = False
chapter = ""
chapters = {}

with open("DRC_xml1.txt") as input_file:
    for line in input_file:
        line = line.strip()
        if '''<h1 id="id00008" style="margin-top: 12em">''' in line:
            title = re.sub(r"[^>]+>([^<]+).*", r"\1", line)
        if '''<h1 id="id00018" style="margin-top: 6em">''' in line:
            in_body = True
        if in_body:
            if "<h2" in line:
                paragraphs = []
                chapter = re.sub(r"[^>]+>([^<]+).*", r"\1", line)
                if chapter not in chapters:
                    chapters[chapter] = [] 
            if "<p" in line:
                current_paragraph = line
                in_paragraph_tag = True
            if "</p>" in line:
                current_paragraph += line 
                current_paragraph = re.sub(r"</?[^>]+>", "", current_paragraph)
                in_paragraph_tag = False
                paragraphs.append(current_paragraph)
                chapters[chapter] = paragraphs
            if in_paragraph_tag: 
                current_paragraph += line 
chapters_word_count = sorted(chapters.items(), key=lambda x: len(x[1]), reverse=True)
# print("\n\n".join(paragraphs))
# print(chapters["CHAPTER II."][0]) # first paragraph of the text
# print(len(chapters))

with open("chapters_paragraph_counts", "w") as output_file:
    for chapter, paragraph in chapters_word_count:
        print(chapter, str(len(paragraph)), file=output_file)