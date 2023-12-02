from flask import Flask, jsonify, request
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow

app=Flask(__name__) #crea el objeto app de la clase Flask
CORS(app) #modulo cors es para q me permita acceder desde el front al back

#CONFIGURO BASE DE DATOS, CON NOMBRE, USUARIO Y CLAVE
app.config['SQLALCHEMY_DATABASE_URI']='mysql+pymysql://root:agus1206@localhost:3306/proyecto'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False 
db=SQLAlchemy(app) # crea el objeto db de la clase SQLALCHEMY
ma=Marshmallow(app) #CREA EL OBJETO MA DE LA CLASE MASHMELLOW


class Cliente(db.Model):  # Producto hereda de db.Model
    """
    Definición de la tabla Clientes en la base de datos.
    La clase clientes hereda de db.Model.
    Esta clase representa la tabla "clientes" en la base de datos.
    """
    id=db.Column(db.Integer, primary_key=True)
    nombre=db.Column(db.String(100))
    apellido=db.Column(db.String(100))
    telefono=db.Column(db.Integer)
    localidad=db.Column(db.String(400))
    direccion=db.Column(db.String(400))
    bolson=db.Column(db.Integer)
    medio_de_pago=db.Column(db.String(400))
    dia_de_entrega=db.Column(db.String(400))

    def __init__(self,nombre,apellido,telefono,localidad,direccion,bolson,medio_de_pago,dia_de_entrega):
        self.nombre=nombre
        self.apellido=apellido
        self.telefono=telefono
        self.localidad=localidad
        self.direccion=direccion
        self.bolson=bolson
        self.medio_de_pago=medio_de_pago
        self.dia_de_entrega=dia_de_entrega

with app.app_context():
    db.create_all()  # Crea todas las tablas en la base de datos

# Definición del esquema para la clase clientes

class ClienteSchema(ma.Schema):
    """
    Esquema de la clase clientes.

    Este esquema define los campos que serán serializados/deserializados
    para la clase clientes.
    """
    class Meta:
        fields=('id','nombre','apellido','telefono','localidad','direccion','bolson','medio_de_pago','dia_de_entrega')

cliente_schema=ClienteSchema()  # Objeto para serializar/deserializar un cliente
clientes_schema=ClienteSchema(many=True)  # Objeto para serializar/deserializar múltiples clientes

@app.route('/cliente',methods=['GET'])
def get_Clientes():
    all_clientes=Cliente.query.all()  # Obtiene todos los registros de la tabla de clientes
    result=clientes_schema.dump(all_clientes)  #  el metodo dump() lo hereda de ma.schema y trae todos los registros de la tabala
    return jsonify(result)  # Retorna el JSON de todos los registros de la tabla
'''
El código que sigue a continuación termina de resolver la API de gestión de productos, a continuación se destaca los principales detalles de cada endpoint, incluyendo su funcionalidad y el tipo de respuesta que se espera.
Endpoints de la API de gestión de productos:
'''

#creo un endpoint para traer solo un cliente

@app.route('/cliente/<id>',methods=['GET'])
def get_cliente(id):
    """
    Retorna un JSON con la información del producto correspondiente al ID proporcionado.
    """
    cliente=Cliente.query.get(id)  # Obtiene el cliente correspondiente al ID recibido
    return cliente_schema.jsonify(cliente)  # Retorna el JSON del cliente

@app.route('/cliente/<id>',methods=['DELETE'])
def delete_cliente(id):
    """
    Endpoint para eliminar un producto de la base de datos.

    Elimina el producto correspondiente al ID proporcionado y retorna un JSON con el registro eliminado.
    """
    cliente=Cliente.query.get(id)  # Obtiene el cliente correspondiente al ID recibido
    db.session.delete(cliente)  # Elimina el cliente de la sesión de la base de datos
    db.session.commit()  # Guarda los cambios en la base de datos
    return cliente_schema.jsonify(cliente)  # Retorna el JSON del cliente eliminado

@app.route('/cliente', methods=['POST'])  # Endpoint para crear un cliente
def create_cliente():
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

@app.route('/cliente/<id>', methods=['PUT'])  # Endpoint para actualizar un producto
def update_cliente(id):
    """
    Endpoint para actualizar un producto existente en la base de datos.

    Lee los datos proporcionados en formato JSON por el cliente y actualiza el registro del producto con el ID especificado.
    Retorna un JSON con el producto actualizado.
    """
    cliente = Cliente.query.get(id)  # Obtiene el producto existente con el ID especificado

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


# Programa Principal
if __name__ == "__main__":
    # Ejecuta el servidor Flask en el puerto 5000 en modo de depuración
    app.run(debug=True, port=5000)
    