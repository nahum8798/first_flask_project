import os
from flask import Flask
from .db import get_db_connection, init_app
# factory function

def create_app():

    # create and configure the app
    app = Flask(__name__)

    app.config.from_mapping(
        DATABASE='proyecto_1'
    )

    # inicializar la base de datos
    init_app(app)

    # import blueprints

    from . import auth
    app.register_blueprint(auth.bp)

    return app