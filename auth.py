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
        db = get_db_connection()
        error = None
        user = db.execute(
            'SELECT FROM users WHERE email = ?', (email,)       # consulta para buscar usuario en la DB
        ).fecthone()

        if not email:                                           # checkeamos que las credenciales sean correctas
            error = "Email incorrecto"
        elif not check_password_hash(user['password'], password):
            error = "Password incorrecto"

        if error is None:           # En el caso de que las credenciales sean correctas procedemos a iniciar la sesión del usuario
            session.clear()
            session['user_id'] = user['id_user']
            return redirect(url_for('index'))

        flash(error)
    return render_template('/login.html')

@bp.before_app_request
def load_logged_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db_connection().execute(
            'SELECT * FROM user WHERE id = ?',(user_id)
        ).fecthone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)
    return wrapped_view





































