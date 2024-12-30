"""
Inicializa la app como un modulo.
Todas las declaraciones podran ser importadas, ya que seran expuestas con el modulo (modular_app)
"""

from flask import Flask

from modular_app.config import ProdConfig

#SQL ALCHEMY permite controlar el modelo entidad relacion desde flask.
from flask_sqlalchemy import SQLAlchemy

#Migrate permite migrar todas las clases creadas como modelo sqlalchemy a la bd,
#este se mantiene actualizado segun el archivos donde se creen los modelos, ya que estos
#heredan la clase (sqlaclhemy.model)
from flask_migrate import Migrate

#Login manager para autenticacion de la app
from flask_login import LoginManager

#Servicio API RESTFULL
from flask_restful import Api

#Liberia para autenticar el API
from flask_jwt_extended import JWTManager
#Inicializa
app = Flask(__name__, static_folder='assets')

#configura
app.config.from_object(ProdConfig)

#Data base
oDb = SQLAlchemy(app)
migrate = Migrate(app=app, db=oDb)

#Crea todas las clases (modelos de slqalchemy) (Tablas) 
#sobre el contexto de la app para poder hacer uso de ello
#with app.app_context():
#    oDb.create_all()

loginMan = LoginManager(app=app)
jwt = JWTManager(app=app)

#API RESOURCES
#TASK
#from modular_app.api.task import TaskAPI
from modular_app.api.task_args_json_body import TaskAPI
from modular_app.api.task_args_json_body import TaskAPIPagination
#TASK UPLOAD DOC
from modular_app.api.task_args_json_body import TaskAPIUpload
#CATEGORIES
from modular_app.api.categories import CategoriesAPI
#TAGS
from modular_app.api.tags import TagAPI


api = Api(app=app)

api.add_resource(TaskAPI, '/api/tasks', '/api/tasks/<int:id>')
api.add_resource(TaskAPIPagination, '/api/tasks/pagination/<int:page>/<int:count>')
api.add_resource(TaskAPIUpload, '/api/tasks/<int:id>/upload')

api.add_resource(CategoriesAPI, '/api/category', '/api/category/<int:id>')

api.add_resource(TagAPI, '/api/tag', '/api/tag/<int:id>')


#BLUEPRINTS
#AUTH
from modular_app.auth.controllers import authRoute
app.register_blueprint(authRoute)

#TASKS
from modular_app.tasks.controllers import taskRoute
app.register_blueprint(taskRoute)