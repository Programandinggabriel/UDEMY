"""
Inicializa la app como un modulo.
Todas las declaraciones podran ser importadas, ya que seran expuestas con el modulo (modular_app)
"""

from flask import Flask
from modular_app.config import ProdConfig
from flask_sqlalchemy import SQLAlchemy 
from flask_migrate import Migrate
from flask_login import LoginManager

#Inicializa
app = Flask(__name__)

#configura
app.config.from_object(ProdConfig)

#Data base
#SQL ALCHEMY permite controlar el modelo entidad relacion desde flask.
oDb = SQLAlchemy(app)

#migrate permite migrar todas las clases creadas como modelo sqlalchemy a la bd, este se mantiene actualizado
#segun el archivo que inicie las clases como (sqlaclhemy.model)
migrate = Migrate(app=app, db=oDb)

#Login manager para tratar la autenticacion en la app
loginMan = LoginManager(app=app)

#Registra blueprints para auth
from modular_app.auth.controllers import authRoute
#Registra blueprints para task
from modular_app.tasks.controllers import taskRoute

app.register_blueprint(taskRoute)
app.register_blueprint(authRoute)

#Crea todas las clases (modelos de slqalchemy) (Tablas) 
#sobre el contexto de la app para poder hacer uso de ello
#with app.app_context():
#    oDb.create_all()