from cryptography.fernet import Fernet
from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('hello.html')

@app.route('/encrypt', methods=['POST'])
def encryptage():
    valeur = request.form.get('valeur')
    key = request.form.get('key')

    if not valeur or not key:
        return "Veuillez fournir une valeur et une clé pour l'encryptage.", 400

    try:
        f = Fernet(key.encode())
        valeur_bytes = valeur.encode()
        token = f.encrypt(valeur_bytes)
        return f"Valeur encryptée : {token.decode()}"
    except Exception as e:
        return f"Erreur lors de l'encryptage : {str(e)}"

@app.route('/decrypt', methods=['GET', 'POST'])
def decryptage():
    if request.method == 'POST':
        key = request.form.get('key')
        token = request.form.get('token')

        if not key or not token:
            return "Veuillez fournir une clé et un token pour le décryptage.", 400

        try:
            f = Fernet(key.encode())
            token_bytes = token.encode()
            valeur_bytes = f.decrypt(token_bytes)
            valeur = valeur_bytes.decode()
            return f"Valeur décryptée : {valeur}"
        except Exception as e:
            return f"Erreur lors du décryptage : {str(e)}"
    
    # Formulaire HTML pour le décryptage
    return '''
        <form method="POST">
            Clé de déchiffrement : <input type="text" name="key"><br>
            Token : <input type="text" name="token"><br>
            <input type="submit" value="Déchiffrer">
        </form>
    '''

if __name__ == "__main__":
    app.run(debug=True)
