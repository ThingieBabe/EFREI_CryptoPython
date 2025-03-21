from cryptography.fernet import Fernet
from flask import Flask, render_template, jsonify
import os

app = Flask(__name__)

# Fonction pour charger ou générer la clé
def load_key():
    if os.path.exists("key.key"):
        with open("key.key", "rb") as key_file:
            return key_file.read()
    else:
        key = Fernet.generate_key()
        with open("key.key", "wb") as key_file:
            key_file.write(key)
        return key

# Chargement ou création de la clé
key = load_key()
f = Fernet(key)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion str -> bytes
    token = f.encrypt(valeur_bytes)  # Encrypt la valeur
    return jsonify({"Valeur encryptée": token.decode()})  # Retourne un JSON

@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        token_bytes = token.encode()  # Conversion str -> bytes
        valeur_bytes = f.decrypt(token_bytes)  # Décrypte le token
        valeur = valeur_bytes.decode()  # Conversion bytes -> str
        return jsonify({"Valeur décryptée": valeur})  # Retourne un JSON
    except Exception as e:
        return jsonify({"Erreur": str(e)}), 400

if __name__ == "__main__":
    app.run(debug=True)
