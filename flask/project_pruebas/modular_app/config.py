#En este archivo se encuentra la configuracion de la app creda con flask.

import os

#Configuración archivos que aceptara la APP FLASK
ALLOWED_EXTENSIONS_FILES = {'pdf', 'jpg', 'jpeg', 'gif', 'png'}
#Función que valida entrada de archivos permititidos
def validate_ext_file(filename:str):
    validate = '.' in filename and filename.lower().rsplit(sep='.', maxsplit=1)[1] in ALLOWED_EXTENSIONS_FILES
    return validate

#Clase que se crea por sel global (las prop de esta se tendran que heredar a cualquier ambiente)
class Config(object):
    UPLOAD_FOLDER = os.path.realpath(path='.') + '/modular_app' #ruta relativa de la app   
    pass

#Configuro base de datos en produccion
class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/UDEMY"
    
    #Clave que permite un unico acceso a el formulario, al senderizado por jinja valida la config de la app flask
    #para encontrar la var GLOBAL O DE ENTORNO (SECRET_KEY)
    SECRET_KEY = "coffe-chiqui-salem"
