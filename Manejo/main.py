from flask import Flask, render_template, jsonify
from string import Template
import connection

data = connection.main()

app = Flask(__name__)

# Se muestran los juegadores en una lista
@app.route('/')
def main():
    return render_template('index.html',data = data)
    
# Ruta para el jugador selecionado 
@app.route('/<n_player>')
def view_player(n_player):
    player = ''
    for p in data:
        if p['id'] == n_player:
            player = p
            break
    return jsonify(player)

app.run()