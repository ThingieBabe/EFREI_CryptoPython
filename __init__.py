from cryptography.fernet import Fernet
from flask import Flask, render_template_string, render_template, jsonify
from flask import render_template
from flask import json
from urllib.request import urlopen
import sqlite3
import os

app = Flask(__name__)

# Fonction pour charger ou générer une clé
def load_key():
    if os.path.exists("secret.key"):
        with open("secret.key", "rb") as key_file:
            return key_file.read()  # Charge la clé existante
    else:
        key = Fernet.generate_key()  # Génère une nouvelle clé
        with open("secret.key", "wb") as key_file:
            key_file.write(key)  # Sauvegarde la clé dans un fichier
        return key

key = load_key()
f = Fernet(key)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return f"Valeur encryptée : {token.decode()}"  # Retourne le token en str

@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        token_bytes = token.encode()  # Conversion str -> bytes
        valeur_bytes = f.decrypt(token_bytes)  # Décrypte le token
        valeur = valeur_bytes.decode()  # Conversion bytes -> str
        return f"Valeur décryptée : {valeur}"
    except Exception as e:
        return f"Erreur lors du décryptage : {str(e)}"

if __name__ == "__main__":
    app.run(debug=True)
