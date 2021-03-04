# -*- coding: utf-8 -*-
import nltk
import pickle
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
#from sklearn.feature_extraction.text import CountVectorizer

app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def main():
    tags=""
    if request.method == 'POST':
        texte = request.form['texte']
        tags = suggestions(texte)
    return render_template("ihm.html", texte=tags)

def suggestions(texte):
    res = pre_processing(texte)
    return res

def pre_processing(texte):
    texte = BeautifulSoup(texte).get_text()
    texte = str.lower(texte)
    
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    texte = tokenizer.tokenize(texte)
    
    filename = 'stopwords.sav'
    stopwords = pickle.load(open(filename, 'rb'))
    texte = [item for item in texte if item not in stopwords]

    ps = nltk.stem.PorterStemmer()
    texte = [ps.stem(item) for item in texte]
    texte =  " ".join(texte)

    #cv = CountVectorizer()
    #filename = 'countvectoriser.sav'
    #cv = pickle.load(open(countvectoriser, 'rb'))
    #res = cv.transform(texte)
    
    return texte


if __name__ == "__main__":
    app.run(debug=True)
