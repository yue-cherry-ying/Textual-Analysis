from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.model_selection import train_test_split
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import re
import os

def preprocess_text(text, stopwords, lemmatizer):
    tokens = re.findall(r"\w+", text)
    tokens = [lemmatizer.lemmatize(token) for token in tokens]
    tokens = [token for token in tokens if token not in stopwords]
    return " ".join(tokens)

if __name__ == "__main__":
    folders = ["talk.politics.mideast", "rec.autos", "comp.sys.mac.hardware", "alt.atheism", 
    "com.os.ms-windows.misc", "rec.sport.hockey", "sci.crypt", "sci.med", "talk.politics.misc", 
    "rec.motorcycles", "comp.windows.x", "comp.graphics", "comp.sys.ibm.pc.hardware", "sci.electronics",
    "talk.politics.guns", "sci.space", "soc.religion.christian", "misc.forsale", "talk.religion.misc"]
    vectorizer = TfidfVectorizer()
    texts = []
    categories = []
    stopwords = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()
    for category in folders:
        for file in os.scandir("20news/" + category):
            with open(file.path, encoding="latin-1") as input_file: # texts have latin-1 encoding
                text = input_file.read()
            text = preprocess_text(text, stopwords, lemmatizer)
            texts.append(text)
            categories.append(category)
    vectorizer = TfidfVectorizer()
    vectorized_texts = vectorizer.fit_transform(texts)
    X_train, X_test, Y_train, Y_test = train_test_split(vectorized_texts, categories, test_size=0.25)
    classifier = MultinomialNB()
    classifier.fit(X_train, Y_train)
    accuracy = classifier.score(X_test, Y_test)
    print(accuracy)

