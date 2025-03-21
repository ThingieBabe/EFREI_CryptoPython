from cryptography.fernet import Fernet
from flask import Flask, render_template
import sqlite3

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

# Génération d'une clé et création de l'objet Fernet
key = Fernet.generate_key()
f = Fernet(key)

@app.route('/encrypt/<string:valeur>')
def encryptage(valeur):
    valeur_bytes = valeur.encode()  # Conversion de la chaîne en bytes
    token = f.encrypt(valeur_bytes)  # Encryptage de la valeur
    return f"Valeur encryptée : {token.decode()}"

@app.route('/decrypt/<string:token>')
def decryptage(token):
    try:
        # Conversion du token en bytes, puis décryptage
        decrypted_bytes = f.decrypt(token.encode())
        decrypted_value = decrypted_bytes.decode()
        return f"Valeur décryptée : {decrypted_value}"
    except Exception as e:
        # En cas d'erreur (exemple : token invalide)
        return f"Erreur lors du décryptage : {str(e)}", 400

if __name__ == "__main__":
    app.run(debug=True)
