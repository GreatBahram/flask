from flask import jsonify
from flask_jwt import jwt_required
from flask_restful import Api

from flask_todo.resources.task import Task, TaskList, CreateTask
from flask_todo.resources.user import User, UserRegisteration, UsersList

from . import api

rest_api = Api(api)


@api.route('')
def index():
    """List of routes for this API."""
    output = {
        'Info': 'GET /api/v1',
        'Register': 'POST /api/v1/account/<username>',
        'Get profile detail': 'GET /api/v1/account',
        'Edit profile': 'PUT /api/v1/account',
        'Delete profile': 'DELETE /api/v1/account',
        'Login and get JSON Web Token': 'POST /api/v1/login',
        'Logout': 'GET /api/v1/account/logout',
        "Get user's tasks": 'GET /api/v1/tasks',
        "Create task": 'POST /api/v1/task',
        "Get task detail": 'GET /api/v1/task/<id>',
        "update task ": 'PUT /api/v1/task/<id>',
        "delete task": 'DELETE /api/v1/task/<id>'
    }
    response = jsonify(output)
    return response

@api.route('/api/v1/account/logout', methods=["GET"])
def logout():
    """Log a user out."""
    return jsonify({'msg': 'Logged out.'})

rest_api.add_resource(UsersList, '/accounts')
rest_api.add_resource(UserRegisteration, '/account/<string:username>')
rest_api.add_resource(User, '/account')

rest_api.add_resource(TaskList, '/tasks')
rest_api.add_resource(CreateTask, '/task')
rest_api.add_resource(Task, '/task/<int:task_id>')
