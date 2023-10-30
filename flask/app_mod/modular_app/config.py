#En este archivo se encuentra la configuracion de la app creda con flask.

class Config(object):
    pass

#Configuro base de datos en produccion
class ProdConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = "postgresql+psycopg2://postgres:postgres@localhost:5432/UDEMY"