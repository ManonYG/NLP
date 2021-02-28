# -*- coding: utf-8 -*-
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route("/", methods=('GET', 'POST'))
def main():
    texte=""
    if request.method == 'POST':
        texte = request.form['texte']
    return render_template("ihm.html", texte=texte)

if __name__ == "__main__":
    app.run(debug=True)
