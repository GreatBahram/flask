# third-party imports
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_jwt import JWT

# local
from flask_todo.config import app_config

db = SQLAlchemy()
bcrypt = Bcrypt()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])


    from flask_todo.models import UserModel, TaskModel
    from flask_todo.security import authenticate, identity

    jwt = JWT(app, authenticate, identity)

    db.init_app(app)
    bcrypt.init_app(app)

    # import and register blueprints
    from .api import api as api_blueprint
    app.register_blueprint(api_blueprint, url_prefix='/api/v1')

    return app

