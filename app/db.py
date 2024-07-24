import mysql.connector
from flask import current_app, g
# configuracion de la conexion a la base de datos MySQL

db_config = {
    'user': 'nahuel',
    'password': 'nM1258menMa',
    'host': 'localhost',
    'database': 'proyecto_1'
}


# establecer conexion
def get_db_connection():

    if 'db' not in g:
        g.db = mysql.connector.connect(**db_config)
    return g.db


# cerrar conexion a base de datos
def close_db():
    db = g.pop('db', None)

    if db is not None:
        db.close()


def init_app(app):
    app.teardown_appcontext(close_db())


