from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import re
import numpy

def find_sections(doc):
    title, filename = doc
    with open(filename) as input_file:
        full_text = input_file.readlines()
        index_start = 0
        if title == "Dracula":
            for line_number, line in enumerate(full_text):
                if "JONATHAN HARKER'S JOURNAL" in line:
                    index_start = line_number - 2
        else:
            for line_number, line in enumerate(full_text):
                if "Chapter 1." in line or "Letter 1" in line or "Chapter I" in line:
                    index_start = line_number
        trimmed_text = full_text[index_start:]
        sections = []
        section = ""
        section_name = ""
        in_section = False
        for line in trimmed_text:
            section_match = re.search(r"\s*(Letter \d+)|(Chapter \S{1,8})\s*\n", line, re.IGNORECASE)
            if section_match:
                if section_name:
                    sections.append((title, section_name, tokenize_doc(section)))
                    if title == "Pride and Prejudice":
                        break
                section = ""
                section_name = section_match.group(0)
                in_section = True 
                continue
            if in_section:
                section += line
    return sections

def tokenize_doc(text_contents):
    english_stopwords = set(stopwords.words("english"))
    tokens = re.findall(r"\w+", text_contents)
    filtered_tokens = []
    for token in tokens:
        if token not in english_stopwords and re.search(r"[!,?;.:]", token) is None:
            filtered_tokens.append(token)
    filtered_text = " ".join(filtered_tokens)
    return filtered_text

if __name__ == "__main__":
    documents = [
        ("Pride and Prejudice", "../texts/pride_and_prejudice.txt"),
        ("Dracula", "../texts/dracula.txt"),
        ("Frankenstein", "../texts/frankenstein.txt"),
        ("Great Expectations", "../texts/great_expectations.txt")
    ]
    all_sections = []
    for doc in documents:
        sections = find_sections(doc)
        all_sections.extend(sections)

    vectorizer = TfidfVectorizer(min_df=0.1, max_df=0.7) # you can play around with this number
    corpus_vectorized = vectorizer.fit_transform(section[2] for section in all_sections)
    results = cosine_similarity(corpus_vectorized) 

    section_score_per_work = {}
    for doc_pos, result_vector in enumerate(results):
        outer_doc_name = all_sections[doc_pos][0]
        for inner_doc_pos in numpy.argsort(result_vector)[::-1]:
            inner_doc_name = all_sections[inner_doc_pos][0]
            if inner_doc_name == "Pride and Prejudice":
                continue # we don't want to compare Pride and Prejudice with itself
            section_name = all_sections[inner_doc_pos][1]
            score = result_vector[inner_doc_pos]
            if inner_doc_name not in section_score_per_work:
                section_score_per_work[inner_doc_name] = {}
            section_score_per_work[inner_doc_name][section_name] = score
        break

    top_score = 0
    top_section = ""
    top_work = ""
    for work, sections in section_score_per_work.items():
        section, score = sorted(sections.items(), key=lambda x: x[1], reverse=True)[0]
        print(f"Top section for {work} is {section} with a score of {score}")
        if score > top_score:
            top_score = score
            top_section = section
            top_work = work
    print("Top section overall is", top_work, top_section, "with a score of", top_score)