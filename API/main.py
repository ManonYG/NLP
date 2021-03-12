# -*- coding: utf-8 -*-
import _pickle as cPickle
import nltk
from flask import Flask, render_template, request
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.ensemble import RandomForestClassifier

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
    res = application_modele(res)
    res = texte_reponse(res)
    return res

def pre_processing(texte):
    texte = BeautifulSoup(texte).get_text()
    texte = str.lower(texte)
    
    tokenizer = nltk.RegexpTokenizer(r'\w+')
    texte = tokenizer.tokenize(texte)
    
    filename = 'stopwords.sav'
    stopwords = cPickle.load(open(filename, 'rb'))
    texte = [item for item in texte if item not in stopwords]

    ps = nltk.stem.PorterStemmer()
    texte = [ps.stem(item) for item in texte]
    texte =  " ".join(texte)

    filename = 'countvectoriser.sav'
    cv = cPickle.load(open(filename, 'rb'))
    res = cv.transform([texte])
    
    filename = 'dim_reduction.sav'
    dim_red = cPickle.load(open(filename, 'rb'))
    res = dim_red.transform(res)
    
    return res

def application_modele(data):
    res = []
    filename = 'modeles.sav'
    rf = cPickle.load(open(filename, 'rb'))
    
    pr = rf.predict_proba(data)
    for i in range(20):
        res.append((pr[i][:,1] >= 0.1).astype('int'))
    
    return res

def texte_reponse(tags):
    filename = 'classes.sav'
    classes = cPickle.load(open(filename, 'rb'))
    
    liste_tags = []
    for i in range(20):
        if tags[i] == 1:
            liste_tags.append(classes[i])
    
    if liste_tags:
        res = "Tags suggérés :"
        for tag in liste_tags:
            res = res + " " + tag + ","
        res = res[:-1]
        res = res + "."
    else:
        res = "Nous n'avons pas pu trouver de tags à vous suggérer."
    
    return res


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=8000)
