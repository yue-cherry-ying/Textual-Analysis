from nltk.stem import WordNetLemmatizer
from nltk.stem.snowball import SnowballStemmer
from nltk.corpus import wordnet
from nltk import pos_tag, Text, tokenize
from re import findall

if __name__ == '__main__':
    wordnet_lemmatizer = WordNetLemmatizer()
    stemmer = SnowballStemmer("english")
    sentence = input("Type in a sentence for lemmatizing and stemming: ")
    tokenized_sentence = findall(r"\w+", sentence)
    tokenized_sentence = pos_tag(tokenized_sentence)
    lemmas = []
    stems = []
    for token, pos in tokenized_sentence:
        lemma = wordnet_lemmatizer.lemmatize(token)
        lemmas.append(lemma)
        stem = stemmer.stem(token)
        stems.append(stem)

    print("LEMMAS", lemmas)
    print("STEMS", stems)

def get_reuters_files(path_to_files):
    """Get content of Reuters files"""
    docs = []
    english_stopwords = set(stopwords.words("english"))
    additional_stopwords = {"quot", "one", "two", "would", "new", "may", "he", "it", "told"}
    english_stopwords.update(additional_stopwords)
    lemmatizer = WordNetLemmatizer()
    for file in os.scandir(path_to_files):
        with open(file.path) as input_file:
            text = input_file.read()
            text = re.sub(r"<[^>]+>", "", text) # remove all tags
        tokens = tokenize.word_tokenize(text)
        text_object = Text(tokens)
        text_with_pos = pos_tag(text_object, tagset="universal")
        filtered_tokens = [word for word in text_with_pos if pos == "NOUN"] # filter based on linguistic features
        filtered_tokens = [lemmatizer.lemmatize(token) for token in tokens if token not in english_stopwords]
        docs.append((file.name, " ".join(filtered_tokens)))
    return docs