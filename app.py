# # Importa las clases Flask, jsonify y request del módulo flask
# from flask import Flask, jsonify, request
# # Importa la clase CORS del módulo flask_cors
# from flask_cors import CORS
# # Importa la clase SQLAlchemy del módulo flask_sqlalchemy
# from flask_sqlalchemy import SQLAlchemy
# # Importa la clase Marshmallow del módulo flask_marshmallow
# from flask_marshmallow import Marshmallow



# app = Flask(__name__) #__name__ es el nombre del archivo, guardo este objeto en la variable app

# @app.route("/") #esto es un decorador
# def hello_world():
#     return "<p>Hello, World!</p>"





from flask import Flask ,jsonify ,request
# del modulo flask importar la clase Flask y los métodos jsonify,request
from flask_cors import CORS       # del modulo flask_cors importar CORS, esto se usa siempre en una API Rest cada vez que necesito conectarme desde el front a una API me da error de seguridad por eso siempre tengo que instalar CORS en cualquier lenguaje. 
from flask_sqlalchemy import SQLAlchemy  #estoy usando los paquetes de sqlalchemy y el de marshmallow, los dos sirven para manejo de la DB. 
from flask_marshmallow import Marshmallow

app=Flask(__name__)  # crear el objeto app de la clase Flask
CORS(app) #modulo cors es para que me permita acceder desde el frontend al backend, le paso a la clase CORS el parametro app. 


# Ahora al objeto app le configuro la base de datos, con el nombre el usuario y la clave
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:root@localhost:3306/proyecto'
# URI de la BBDD                          driver de la BD  user:clave@URLBBDD/nombreBBDD
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False #none
db= SQLAlchemy(app)   #crea el objeto db de la clase SQLAlquemy
ma=Marshmallow(app)   #crea el objeto ma de de la clase Marshmallow

#---------A PARTIR DE ACÁ DEFINO LOS MODELOS DE LA BD ---------- 
# defino la tabla, si tuviera más de una, ej usuarios, clientes, productos etc, las defino todas acá. 
class Producto(db.Model):   # la clase Producto hereda de db.Model. Acá usamos métodos del objeto db que es de la clase SQLAlchemy que me van a permitir definir los campos de la BD, se que es método por tener db.metodo    
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    nombre=db.Column(db.String(100))
    precio=db.Column(db.Integer)
    stock=db.Column(db.Integer)
    imagen=db.Column(db.String(400))
    def __init__(self,nombre,precio,stock,imagen):   #crea el  constructor de la clase. Acá estoy diciendo, "el nombre que recibis como parámetro asignaselo al atributo nombre y así con todos"
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento, como es primary key me despreocupo. 
        self.precio=precio
        self.stock=stock
        self.imagen=imagen 



    #  si hay que crear mas tablas , se hace aqui



#--------- ahora le digo que cree la tabla. Si ya esta creada py y flask se avivan que ya está y no la crea de nuevo cada vez que interpreto el proyecto (que corro py)
with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class ProductoSchema(ma.Schema): #acá creo la clase productoSchema
    class Meta:
        fields=('id','nombre','precio','stock','imagen') #defino los campos de mi tabla




producto_schema=ProductoSchema()            # El objeto producto_schema es para crear un producto
productos_schema=ProductoSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto. 




# crea los endpoint o rutas (json) los "Controladores"
@app.route('/productos',methods=['GET']) #a la URL del servidor de flask le voy a agregar /productos y el método que quiero, acá GET. Le digo "traeme una consulta de todos los productos, almacenalo en en el objeto all_productos, hace un dump y almacena el resultado y ese resultado convertilo a JSON y devolvemelo"
def get_Productos():
    all_productos=Producto.query.all()         # el metodo query.all() lo hereda de db.Model
    result=productos_schema.dump(all_productos)  # el metodo dump() lo hereda de ma.schema y
                                                 # trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla

#cada vez que yo llame a la URL del servidor/flask con el método get me trae un json con todos los productos. Acá devuelve una lista con muchos productos. 



#acá creamos un endpoint para traer un solo producto, el id se lo paso como parámetro, '/productos/<id>' es la ruta, le digo con qué método. 
@app.route('/productos/<id>',methods=['GET'])
def get_producto(id): #acá llamo a la función get_producto con id. 
    producto=Producto.query.get(id)
    return producto_schema.jsonify(producto)   # retorna el JSON de un solo producto recibido como parametro que lo busca por id. 



#creo el endpoint para borrar. "en la ruta/productos/id borrame tal producto en particular"
@app.route('/productos/<id>',methods=['DELETE'])
def delete_producto(id):
    producto=Producto.query.get(id) #primero lo traigo y lo guardo en una variable. Despues cuando ya lo tiene lo borro con delete y finalmente con .commit le digo confirma el cambio y traeme en un JSON el producto que borré. 
    db.session.delete(producto)
    db.session.commit()
    return producto_schema.jsonify(producto)   # me devuelve un json con el registro eliminado


@app.route('/productos', methods=['POST']) # crea ruta o endpoint
def create_producto():
    #print(request.json)  # request.json contiene el json que envio el cliente
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']
    new_producto=Producto(nombre,precio,stock,imagen)
    db.session.add(new_producto)
    db.session.commit()
    return producto_schema.jsonify(new_producto)


@app.route('/productos/<id>' ,methods=['PUT'])
def update_producto(id):
    producto=Producto.query.get(id)
 
    nombre=request.json['nombre']
    precio=request.json['precio']
    stock=request.json['stock']
    imagen=request.json['imagen']


    producto.nombre=nombre
    producto.precio=precio
    producto.stock=stock
    producto.imagen=imagen


    db.session.commit()
    return producto_schema.jsonify(producto)
 


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000, esto significa que me va a crear un servidor en el puerto 5000 asi que a la URL del servidor de Flask le voy a agregar