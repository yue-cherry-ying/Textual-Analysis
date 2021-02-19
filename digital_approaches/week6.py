# Yue "Cherry" Ying
# Python Exercise for Tuesday Feb. 16th

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy
import re
from nltk.corpus import stopwords

def read_and_tokenize_doc(filepath, english_stopwords): 
    chapters = {}
    chapter_name = ""
    with open(filepath) as input_file: 
        if filepath  == "../texts/dracula.txt":
            filename = "Dracula"
        elif filepath == "../texts/pride_and_prejudice.txt":
            filename = "Pride and Prejudice"
        elif filepath == "../texts/frankenstein.txt":
            filename = "Frankenstein"
        elif filepath == "../texts/great_expectations.txt":
            filename = "Great Expectations"
        for line in input_file:
            line = line.strip()
            if re.match(r"CHAPTER ", line) or re.match(r"Chapter ", line) or re.match(r"Letter ", line):
                chapter_name = line
                if chapter_name not in chapters:
                    chapters[chapter_name] = ""
                continue
                elif chapter_name == "":
                    continue
            tokens = re.findall(r"\w+", line)   
            filtered_tokens = []    
            for token in tokens:        
                if token not in english_stopwords and re.search(r"[!,?;.:]", token) is None:            
                    filtered_tokens.append(token)    
            filtered_text = " ".join(filtered_tokens) 
            chapters[chapter_name] += filtered_text
        tuple_list = [(filename, chapter_name, filtered_text) for chapter_name, filtered_text in chapters.items()]
        return tuple_list

if __name__ == "__main__":
    english_stopwords = set(stopwords.words("english"))

    expectations = read_and_tokenize_doc("../texts/great_expectations.txt", english_stopwords)
    pride = read_and_tokenize_doc("../texts/pride_and_prejudice.txt", english_stopwords)
    frankenstein = read_and_tokenize_doc("../texts/frankenstein.txt", english_stopwords)
    dracula = read_and_tokenize_doc("../texts/dracula.txt", english_stopwords)
    chapter1_pride = pride[0]
    clean_docs = [str(chapter1_pride), str(expectations), str(frankenstein), str(dracula)]
    
    vectorizer = TfidfVectorizer(min_df=2) 
    corpus_vectorized = vectorizer.fit_transform(clean_docs)
    results = cosine_similarity(corpus_vectorized) 
    print(results)
    for doc_pos, result_vector in enumerate(results): 
        outer_doc_name = "Pride and Prejudice"
        for doc_index in numpy.argsort(result_vector)[::-1]:
            inner_doc_name = clean_docs[doc_index][0] 
            score = result_vector[doc_index]
            if outer_doc_name != inner_doc_name:
                print(f"Most similar document to {outer_doc_name} is {inner_doc_name} with a score of {score}")
