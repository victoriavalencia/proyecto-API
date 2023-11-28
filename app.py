from flask import Flask

app = Flask(__name__) #__name__ es el nombre del archivo, guardo este objeto en la variable app

@app.route("/") #esto es un decorador
def hello_world():
    return "<p>Hello, World!</p>"