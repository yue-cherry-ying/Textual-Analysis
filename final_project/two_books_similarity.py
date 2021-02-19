from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity
import re
import numpy

# -------------------------------------------------------
# Similarity between sections in Book I and Book II

def find_sections(doc):
    title, filename = doc
    with open(filename) as input_file:
        full_text = input_file.readlines()
        index_start = 0
        if title == "Book I":
            for line_number, line in enumerate(full_text):
                if "CHAPTER I." in line:
                    index_start = line_number
        else:
            for line_number, line in enumerate(full_text):
                if "CHAPTER XXV." in line:
                    index_start = line_number
        trimmed_text = full_text[index_start:]
        sections = []
        section = ""
        section_name = ""
        in_section = False
        for line in trimmed_text:
            section_match = re.search(r"(CHAPTER \S{1,8}).\s*\n", line, re.IGNORECASE)
            if section_match:
                if section_name:
                    sections.append((title, section_name, tokenize_doc(section)))
                    # if title == "Book I":
                    #     break
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
        ("Book I", "DRC_BookI.txt"),
        ("Book II", "DRC_BookII.txt")
    ]
    all_sections = []
    for doc in documents:
        sections = find_sections(doc)
        all_sections.extend(sections)

    vectorizer = TfidfVectorizer(min_df=2)
    corpus_vectorized = vectorizer.fit_transform(section[2] for section in all_sections)
    results = cosine_similarity(corpus_vectorized) 

    section_score_per_work = {}
    for doc_pos, result_vector in enumerate(results):
        outer_doc_name = all_sections[doc_pos][0]
        for inner_doc_pos in numpy.argsort(result_vector)[::-1]:
            inner_doc_name = all_sections[inner_doc_pos][0]
            if inner_doc_name == "Book I":
                continue
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

# -------------------------------------------------------
# Similarity score between Book I and Book II

def read_and_tokenize_doc(filename, stopwords):
    with open(filename) as text:
        text_contents = text.read()
    tokens = re.findall(r"\w+", text_contents)
    filtered_tokens = []
    for token in tokens:
        if token not in english_stopwords and re.search(r"[!,?;.:]", token) is None:
            filtered_tokens.append(token)
    filtered_text = " ".join(filtered_tokens)
    return filtered_text

if __name__ == "__main__":
    english_stopwords = set(stopwords.words("english"))
    documents = [
        ("Book I", "DRC_BookI.txt"),
        ("Book II", "DRC_BookII.txt")
    ]
    vectorizer = TfidfVectorizer(min_df=2)    
    corpus_vectorized = vectorizer.fit_transform(doc[1] for doc in documents)    
    results = cosine_similarity(corpus_vectorized)
    for doc_pos, result_vector in enumerate(results):        
        outer_doc_name = documents[doc_pos][0]       
        for inner_doc_pos in numpy.argsort(result_vector)[::-1]:       
            inner_doc_name = documents[inner_doc_pos][0]  
            # if inner_doc_name == "Book I":
            #     continue         
            score = result_vector[inner_doc_pos]           
            if inner_doc_name != outer_doc_name:                
                print(f"The similarity between {outer_doc_name} and {inner_doc_name} is with a score of {score}")                
                break