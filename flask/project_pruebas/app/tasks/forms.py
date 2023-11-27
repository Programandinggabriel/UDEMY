"""Flask-WTF Esta lib facilita la integracion de forms y el server, debido a que permite controlar los forms 
    directamente con backend"""

from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import InputRequired

#Clase de formulario para task
class TaskForm(FlaskForm):
    name = StringField(label='Name', validators=[InputRequired()])