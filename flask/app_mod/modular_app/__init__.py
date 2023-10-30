"""
Inicializa la app como un modulo.
Todas las declaraciones podran ser importadas, ya que seran expuestas con el modulo (modular_app)
"""

from flask import Flask, render_template, request
from modular_app.config import ProdConfig
from flask_sqlalchemy import SQLAlchemy 

#Inicializa
app = Flask(__name__)

#configura
app.config.from_object(ProdConfig)

#Data base
#SQL ALCHEMY permite controlar el modelo entidad relacion desde flask.
oDb = SQLAlchemy(app)

#Registra blueprints para task
from modular_app.tasks.controllers import taskRoute
app.register_blueprint(taskRoute)

#create db
with app.app_context():
    oDb.create_all()

@app.route('/')
def prueba_jinja():
    name = request.args.get(key='name', default='', type=str)
    return render_template(template_name_or_list='index.html', name=name)