import functools

from flask import (
    Blueprint, flash, g, redirect,url_for ,render_template, request, session
)

from werkzeug.security import generate_password_hash, check_password_hash

from .db import get_db_connection

bp = Blueprint('auth', __name__, url_prefix='/auth') # creamos un blueprint auth con un prefijo de url

# vista de registro


@bp.route('/register', methods=('GET','POST'))
def register():

    if request.method == 'POST':
        # leemos los datos pasados por el formulario
        username = request.form['username']
        userlastname = request.form['userlastname']
        email = request.form['userlastname']
        password = request.form['username']

        # abrimos conexion con la base de datos
        db = get_db_connection()
        error = None

        if not username:
            error = "El nombre del usuario es requerido"
        elif not userlastname:
            error = "El apellido del usuario es requerido"
        elif not email:
            error = "El email es requerido"
        elif not password:
            error = "La contraseña es requerida"

        if error is None:
            try:
                db.execute(
                    "INSERT INTO users (user_name, user_lastname, user_email, user_password) VALUES (?, ?, ?. ?)",
                    (username, userlastname, email, generate_password_hash(password))
                )
                db.commit()
            except db.IntegrityError:
                error = f"El usuario {username} ya esta registrado"
            else:
                return redirect(url_for('auth.login'))

        flash(error)

    return render_template('register.html')


# vista de login
@bp.route('/login', methods=('GET','POST'))
def login():

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']








































