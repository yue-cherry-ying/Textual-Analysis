import spacy
spacy.load('en_core_web_sm')
from spacy.lang.en import English
parser = English()
import nltk
# nltk.download('wordnet')
from nltk.corpus import wordnet as wn
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import stopwords
import re
import random

# -------------------------------------
# Text Cleaning

def get_lemma(word):
    lemma = wn.morphy(word)
    if lemma is None:
        return word
    else:
        return lemma

def get_lemma2(word):
    return WordNetLemmatizer().lemmatize(word)

def prepare_text_for_lda(text):
    english_stopwords = set(stopwords.words("english"))
    tokens = re.findall(r"\w+", text)
    filtered_tokens = []
    for token in tokens:
        if token not in english_stopwords and re.search(r"[!,?;.:]", token) is None and len(token) > 3: # play around the len(token), let it to > 3 or > 4
            token = get_lemma(token)
            filtered_tokens.append(token)
    filtered_text = " ".join(filtered_tokens)
    return filtered_text

text_data = []
in_the_text = False
with open('DRC_BookI.txt') as f:
    for line in f:
        if re.search(r"(CHAPTER \S{1,8}).\s*\n", line, re.IGNORECASE):
            in_the_text = True
        if in_the_text:
            tokens = prepare_text_for_lda(line)
            if random.random() > .99:
                if len(tokens) != 0:
                    # print(tokens)
                    text_data.append(tokens)
    # print(text_data[:5])

# ---------------------------------
# LDA with Gensim

import gensim
from gensim import corpora
from gensim.utils import simple_preprocess
import pickle

text_tokenized = [simple_preprocess(text) for text in text_data]
dictionary = corpora.Dictionary()
corpus = [dictionary.doc2bow(text, allow_update=True) for text in text_tokenized]
pickle.dump(corpus, open('corpus.pkl', 'wb'))
dictionary.save('dictionary.gensim')

# try 5 topics in the data
NUM_TOPICS = 5
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = NUM_TOPICS, id2word=dictionary, passes=15)
ldamodel.save('model5.gensim')

topics = ldamodel.print_topics(num_words=8) # adjust the num_words, try num_words=4, 6, 8
# for topic in topics:
#     print(topic)

new_doc = 'The Ladies are the Dominant Figures in the Chia Family, and They Run the House'
new_doc = simple_preprocess(new_doc)
new_doc_bow = dictionary.doc2bow(new_doc)
# print(new_doc_bow)
# print(ldamodel.get_document_topics(new_doc_bow))

# find 3 topics in the data
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 3, id2word=dictionary, passes=15)
ldamodel.save('model3.gensim')
topics = ldamodel.print_topics(num_words=4)
# for topic in topics:
#     print(topic)

# find 10 topics in the data
ldamodel = gensim.models.ldamodel.LdaModel(corpus, num_topics = 10, id2word=dictionary, passes=15)
ldamodel.save('model10.gensim')
topics = ldamodel.print_topics(num_words=4)
# for topic in topics:
#     print(topic)

# -----------------------------------
# pyLDAvis: designed to help users interpret the topics in a topic model that has been fit to a corpus of text data. 
# The package extracts information from a fitted LDA topic model to inform an interactive web-based visualization.
import pyLDAvis.gensim

# visualizing 5 topics
dictionary = gensim.corpora.Dictionary.load('dictionary.gensim')
corpus = pickle.load(open('corpus.pkl', 'rb'))
lda = gensim.models.ldamodel.LdaModel.load('model5.gensim')

lda_display = pyLDAvis.gensim.prepare(lda, corpus, dictionary, sort_topics=False)
# pyLDAvis.display(lda_display)
pyLDAvis.save_html(lda_display, 'lda5.html')

# visualizing 3 topics
lda3 = gensim.models.ldamodel.LdaModel.load('model3.gensim')
lda_display3 = pyLDAvis.gensim.prepare(lda3, corpus, dictionary, sort_topics=False)
# pyLDAvis.display(lda_display3)
pyLDAvis.save_html(lda_display3, 'lda3.html')

# visualizing 10 topics
lda10 = gensim.models.ldamodel.LdaModel.load('model10.gensim')
lda_display10 = pyLDAvis.gensim.prepare(lda10, corpus, dictionary, sort_topics=False)
# pyLDAvis.display(lda_display10)
pyLDAvis.save_html(lda_display10, 'lda10.html')