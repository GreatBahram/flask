"""Script for initializing your database.

Note that dropping your existing tables is an opt-in operation.
If you want to drop tables before you create tables, set an environment
variable called "DEVELOPMENT" to be "True".
"""
import os

from flask_todo import db, create_app
from flask_todo.models import UserModel, TaskModel

app = create_app('development')

db.app = app

if bool(os.environ.get('DEVELOPMENT', '')):
    db.drop_all()
db.create_all()
