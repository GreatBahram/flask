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
        username = current_identity
        return {'Tasks': username.tasks}


class CreateTask(Resource):
    @jwt_required()
    def post(self):
        username = current_identity
        print(username)

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
    def get(self, task_id):
        """Get the detail for an individual profile."""
        task = TaskModel.find_by_id(task_id)
        if task:
            return task.to_dict()
        return {'message': 'Task not found'}, 404

    def put(self, task_id):
        pass

    def delete(self, task_id):
        """."""
        task = TaskModel.query.filter_by(id=task_id).first()
        if task:
            task.delete_from_db()
            return {'message': f'Task {task_id} has been deleted.'}, 201
        return {'message': 'Task not found'}, 404
        
