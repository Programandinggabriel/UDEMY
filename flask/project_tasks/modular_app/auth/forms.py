from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField, EmailField
from wtforms.validators import input_required, equal_to

#Clase formulario registro
class registerForm(FlaskForm):
    userName = StringField(label='Usuario', validators=[input_required()])
    firtsName = StringField(label='Primer nombre', validators=[input_required()])
    secondName = StringField(label='Segundo nombre', validators=[input_required()])
    email = EmailField(label='Email', validators=[input_required()])
    password = PasswordField(label='Contraseña', validators=[input_required(),
                                                             equal_to(fieldname='confirmPswd', message='Las contraseñas no coinciden')])
    confirmPswd = PasswordField(label='Confirmar contraseña', validators=[input_required()])
    

#Clase formulario login
class loginForm(FlaskForm):
    userName = StringField(label='usuario', validators=[input_required()])
    password = PasswordField(label='contraseña', validators=[input_required()])