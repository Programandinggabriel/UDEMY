"""Flask-WTF Esta lib facilita la integracion de forms y el server, debido a que permite controlar los forms 
    directamente con backend"""

from flask_wtf import FlaskForm
from wtforms import StringField, FileField, SelectField, HiddenField
from wtforms.validators import InputRequired

#Clase de formulario para task
class TaskForm(FlaskForm):
    name = StringField(label='Name', validators=[InputRequired()])
    file = FileField(label='Document',) #optional
    category = SelectField(label='Category', validators=[InputRequired()])

class TaskAddTagForm(FlaskForm):
    tag = SelectField(label='Tag',)

class TaskDeleteTagForm(FlaskForm):
    tag = HiddenField(label='Tag',)