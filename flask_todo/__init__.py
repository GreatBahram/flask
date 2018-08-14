# third-party imports
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

# local
from flask_todo.config import app_config

db = SQLAlchemy()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])

    db.init_app(app)

    return app

