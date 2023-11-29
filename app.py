# Importa las clases Flask, jsonify y request del módulo flask
from flask import Flask, jsonify, request
# Importa la clase CORS del módulo flask_cors
from flask_cors import CORS
# Importa la clase SQLAlchemy del módulo flask_sqlalchemy
from flask_sqlalchemy import SQLAlchemy
# Importa la clase Marshmallow del módulo flask_marshmallow
from flask_marshmallow import Marshmallow



app = Flask(__name__) #__name__ es el nombre del archivo, guardo este objeto en la variable app

@app.route("/") #esto es un decorador
def hello_world():
    return "<p>Hello, World!</p>"