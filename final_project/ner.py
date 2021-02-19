import spacy
nlp = spacy.load("en_core_web_sm")
from nltk.corpus import stopwords
import nltk
import re

# Process whole documents
with open('DRC_BookI.txt') as f:
    text = f.read()
    english_stopwords = set(stopwords.words("english"))
    tokens = re.findall(r"\w+", text)
    filtered_tokens = []
    for token in tokens:
        if token not in english_stopwords and re.search(r"[!,?;.:]", token) is None:
            filtered_tokens.append(token)
    text = " ".join(filtered_tokens)

doc = nlp(text)

# Analyze syntax
# print("Noun phrases:", [chunk.text for chunk in doc.noun_chunks])
# print("Verbs:", [token.lemma_ for token in doc if token.pos_ == "VERB"])

# Find named entities, phrases and concepts
# for entity in doc.ents:
#     print(entity.text, entity.label_)

# Find all persons
# person = []
# for entity in doc.ents:
#     if entity.label_ == "PERSON":
#         if entity.text not in person:
#             person.append(entity.text)
# print("Person:", person)

# Find all locations
# location = []
# for entity in doc.ents:
#     if entity.label_ == "GPE":
#         if entity.text not in location:
#             location.append(entity.text)
# print("Location:", location)

# Find all dates
# date = []
# for entity in doc.ents:
#     if entity.label_ == "DATE":
#         if entity.text not in date:
#             date.append(entity.text)
# print("Date:", date)

# Find all organizations
# org = []
# for entity in doc.ents:
#     if entity.label_ == "ORG":
#         if entity.text not in org:
#             org.append(entity.text)
# print("Organization:", org)