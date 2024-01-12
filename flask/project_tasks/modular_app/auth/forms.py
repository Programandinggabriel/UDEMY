from flask_wtf import FlaskForm

from wtforms import StringField, PasswordField
from wtforms.validators import input_required, equal_to

#Clase formulario registro
class registerForm(FlaskForm):
    userName = StringField(label='usuario', validators=[input_required()])
    password = PasswordField(label='contraseña', validators=[input_required(),
                                                             equal_to(fieldname='confirmPswd', message='Las contraseñas no coinciden')
                                                             ])
    confirmPswd = PasswordField(label='confirmar contraseña', validators=[input_required()])

#Clase formulario login
class loginForm(FlaskForm):
    userName = StringField(label='usuario', validators=[input_required()])
    password = PasswordField(label='contraseña', validators=[input_required()])