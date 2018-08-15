# third-party imports
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from flask_todo.models.user import UserModel
from flask_todo.models.task import TaskModel
from flask_todo import db

INCOMING_DATE_FMT = '%d/%m/%Y %H:%M:%S'

class TaskList(Resource):
    @jwt_required()
    def get(self):
        """List all of the tasks for one user."""
        username = current_identity
        return {'Tasks': [task.to_dict()for task in username.tasks]}


class CreateTask(Resource):
    @jwt_required()
    def post(self):
        username = current_identity
        parser = reqparse.RequestParser()
        parser.add_argument('name', required=True, help="This field cannot be blank!")
        parser.add_argument('note', required=True, help="This field cannot be blank!")
        parser.add_argument('due-date', help="This field cannot be blank!")
        parser.add_argument('completed', help="This field cannot be blank!")
        data = parser.parse_args()
        try:
            task = TaskModel(name=data['name'], note=data['note'],user=username) 
            task.save_to_db()
            return task.to_dict(), 201
        except:
            return {'message': 'Something wrong happend.'}, 400


class Task(Resource):
    @jwt_required()
    def get(self, task_id):
        """Get the detail for one task if that task belongs to the provided user."""
        task = TaskModel.query.filter_by(id=task_id).first()
        current_user_tasks = current_identity.tasks
        if task and task in current_user_tasks:
            return task.to_dict()
        return {'message': 'Task not found'}, 404

    def put(self, task_id):
        """Update one task if that task belongs to the provided user."""
        pass

    @jwt_required()
    def delete(self, task_id):
        """Delete one task if that task belongs to the provided user."""
        task = TaskModel.query.filter_by(id=task_id).first()
        current_user_tasks = current_identity.tasks
        if task and task in current_user_tasks:
            task.delete_from_db()
            return {'message': f'Task {task_id} has been deleted.'}, 201
        return {'message': 'Task not found'}, 404
