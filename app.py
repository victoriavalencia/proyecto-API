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
class Cliente(db.Model):   # la clase Producto hereda de db.Model. Acá usamos métodos del objeto db que es de la clase SQLAlchemy que me van a permitir definir los campos de la BD, se que es método por tener db.metodo    Definición de la tabla clientes en la db. Esta clase representa la tabla cliente en la db. 
    id=db.Column(db.Integer, primary_key=True)   #define los campos de la tabla
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    apellido=db.Column(db.String(100))
    telefono=db.Column(db.Integer)
    localidad=db.Column(db.String(100))
    direccion=db.Column(db.String(400))
    bolson=db.Column(db.Integer)
    medio_de_pago=db.Column(db.String(45))
    dia_de_entrega=db.Column(db.String(45))


    def __init__(self,nombre,apellido,telefono,localidad,direccion, bolson, medio_de_pago, dia_de_entrega):   #crea el  constructor de la clase. Acá estoy diciendo, "el nombre que recibis como parámetro asignaselo al atributo nombre y así con todos"
        self.nombre=nombre   # no hace falta el id porque lo crea sola mysql por ser auto_incremento, como es primary key me despreocupo. 
        self.apellido=apellido
        self.telefono=telefono
        self.localidad=localidad 
        self.direccion=direccion
        self.bolson=bolson
        self.medio_de_pago=medio_de_pago
        self.dia_de_entrega= dia_de_entrega



    #  si hay que crear mas tablas , se hace aqui



#--------- ahora le digo que cree la tabla. Si ya esta creada py y flask se avivan que ya está y no la crea de nuevo cada vez que interpreto el proyecto (que corro py)
with app.app_context():
    db.create_all()  # aqui crea todas las tablas
#  ************************************************************
class ClienteSchema(ma.Schema): #acá creo la clase productoSchema
    class Meta:
        fields=('id','nombre','apellido','telefono','localidad', 'direccion', 'bolson', 'medio_de_pago', 'dia_de_entrega') #defino los campos de mi tabla




cliente_schema=ClienteSchema()            # El objeto producto_schema es para crear un producto
clientes_schema=ClienteSchema(many=True)  # El objeto productos_schema es para traer multiples registros de producto. 



# crea los endpoint o rutas (json) los "Controladores"
@app.route('/cliente',methods=['GET']) #a la URL del servidor de flask le voy a agregar /productos y el método que quiero, acá GET. Le digo "traeme una consulta de todos los productos, almacenalo en en el objeto all_productos, hace un dump y almacena el resultado y ese resultado convertilo a JSON y devolvemelo"
def get_Clientes():
    all_clientes=Cliente.query.all()         # el metodo query.all() lo hereda de db.Model
    result=clientes_schema.dump(all_clientes)  # el metodo dump() lo hereda de ma.schema y trae todos los registros de la tabla
    return jsonify(result)                       # retorna un JSON de todos los registros de la tabla

#cada vez que yo llame a la URL del servidor/flask con el método get me trae un json con todos los productos. Acá devuelve una lista con muchos productos. 

'''
El código que sigue a continuación termina de resolver la API de gestión de productos, a continuación se destaca los principales detalles de cada endpoint, incluyendo su funcionalidad y el tipo de respuesta que se espera.
Endpoints de la API de gestión de productos:
''' 


#acá creamos un endpoint para traer un solo cliente, el id se lo paso como parámetro, '/productos/<id>' es la ruta, le digo con qué método. 
@app.route('/cliente/<id>',methods=['GET'])
def get_Clientes(id): #acá llamo a la función get_producto con id. 
    cliente=Cliente.query.get(id)
    return cliente_schema.jsonify(cliente)   # retorna el JSON de un solo producto recibido como parametro que lo busca por id. 



#creo el endpoint para borrar. "en la ruta/productos/id borrame tal producto en particular"
@app.route('/cliente/<id>',methods=['DELETE'])
def delete_cliente(id):
    cliente=Cliente.query.get(id) #primero lo traigo y lo guardo en una variable. Despues cuando ya lo tiene lo borro con delete y finalmente con .commit le digo confirma el cambio y traeme en un JSON el producto que borré. 
    db.session.delete(cliente)
    db.session.commit()
    return cliente_schema.jsonify(cliente)   # me devuelve un json con el registro eliminado


@app.route('/cliente', methods=['POST']) # crea ruta o endpoint
def create_cliente():
        
    #print(request.json)  # request.json contiene el json que envio el cliente
        """
    Endpoint para crear un nuevo cliente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y crea un nuevo registro del cliente  en la base de datos.
    Retorna un JSON con el nuevo producto creado. telefono, localidad, direccion, bolson, medio_de_pago, dia_de_entrega):
    """
        nombre = request.json['nombre']  
        apellido = request.json['apellido']  
        telefono = request.json['telefono']  
        localidad = request.json['localidad']  
        direccion = request.json['direccion'] 
        bolson = request.json['bolson'] 
        medio_de_pago = request.json['medio_de_pago'] 
        dia_de_entrega = request.json['dia_de_entrega'] 
        new_cliente = Cliente(nombre, apellido, telefono, localidad, direccion, bolson, medio_de_pago, dia_de_entrega )  # Crea un nuevo objeto Producto con los datos proporcionados
        db.session.add(new_cliente)  # Agrega el nuevo producto a la sesión de la base de datos
        db.session.commit()  # Guarda los cambios en la base de datos
        return clientes_schema.jsonify(new_cliente)  # Retorna el JSON del nuevo producto creado


@app.route('/cliente/<id>' ,methods=['PUT'])
def update_cliente(id):
    cliente=Cliente.query.get(id)
 
        # Actualiza los atributos del producto con los datos proporcionados en el JSON
    nombre = request.json['nombre']  
    apellido = request.json['apellido']  
    telefono = request.json['telefono']  
    localidad = request.json['localidad']  
    direccion = request.json['direccion'] 
    bolson = request.json['bolson'] 
    medio_de_pago = request.json['medio_de_pago'] 
    dia_de_entrega = request.json['dia_de_entrega'] 

    db.session.commit()  # Guarda los cambios en la base de datos
    return clientes_schema.jsonify(cliente)  # Retorna el JSON del producto actualizado


# programa principal *******************************
if __name__=='__main__':  
    app.run(debug=True, port=5000)    # ejecuta el servidor Flask en el puerto 5000, esto significa que me va a crear un servidor en el puerto 5000 asi que a la URL del servidor de Flask le voy a agregar