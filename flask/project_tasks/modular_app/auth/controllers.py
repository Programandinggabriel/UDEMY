from flask import g, Blueprint, flash, redirect, render_template, request, url_for

from flask_login import current_user, login_user, logout_user

from modular_app import loginMan
from modular_app.auth import models, forms, sql_operations

authRoute = Blueprint(name='auth', import_name=__name__)

@loginMan.user_loader
def load_user(id):
    return models.User.query.get(ident=id)

@authRoute.before_request
#funcion necesaria por flask login para establecer el usuario
def get_current_user():
    g.user = current_user


@authRoute.route(rule='/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash("Usuario previamente autenticado", category='info')
        return redirect(location='tasks.index')
    
    frmRegister = forms.registerForm()

    if request.method == 'GET':
        return render_template('auth/register.html', frmRegister=frmRegister)
    elif request.method == 'POST':
        if frmRegister.validate_on_submit():
            username = frmRegister.userName.data
            password = frmRegister.password.data

            user_exist = sql_operations.getUserByUserName(username=username)

            if user_exist:
                frmLogin = forms.loginForm()

                flash('El usuario ya se encuentra registrado, intente con otro')
                return render_template('auth/login.html', frmLogin=frmLogin)
            else:
                createUser = sql_operations.createUser(username=username, password=password)
                flash(f'El usuario {createUser.userName} fue creado con exito')

        #Errores en formulario
        if frmRegister.errors:
            flash(frmRegister.errors, 'danger')

    return render_template('auth/register.html', frmRegister=frmRegister)

@authRoute.route(rule='/login', methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        flash("Usuario previamente autenticado", category='info')
        return redirect(url_for('tasks.index'))
    
    frmLogin = forms.loginForm()

    if request.method == "GET":
        return render_template('auth/login.html', frmLogin=frmLogin)
    elif request.method == "POST":
        if frmLogin.validate_on_submit():
            username = frmLogin.userName.data
            password = frmLogin.password.data

            user = sql_operations.getUserByUserName(username)
            
            if user:
                if user.validatePasword(password):
                    login_user(user=user)
                    return redirect(location=url_for('tasks.index'))
                else:
                    flash(message="Usuario o contraseña incorrectos")
                    return render_template('auth/login.html', frmLogin=frmLogin)
            else:
                flash(message="Usuario o contraseña incorrectos")
                return render_template('auth/login.html', frmLogin=frmLogin)
                
@authRoute.route('/logout', methods=["POST"])
def logout():
    logout_user()
    return url_for('auth.login') 