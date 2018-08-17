# third-party imports
from flask_jwt import current_identity, jwt_required
from flask_restful import Resource, reqparse
from sqlalchemy.exc import IntegrityError

# local imports
from flask_todo import db
from flask_todo.models.task import TaskModel
from flask_todo.models.user import UserModel


class User(Resource):
    @jwt_required()
    def get(cls):
        """Get the detail for an individual profile."""
        username = current_identity.username
        user = UserModel.query.filter_by(username=username).first()
        if user:
            return user.to_dict()
        return {"message": "User not found"}

    @jwt_required()
    def put(self):
        """Add a new user profile if it doesn't already exist."""
        username = current_identity.username

        parser = reqparse.RequestParser()
        parser.add_argument('username', required=True, help="This field cannot be blank!")
        parser.add_argument('email', required=True, help="This field cannot be blank!")
        data = parser.parse_args()
        user = UserModel.find_by_username(username)
        if user:
            if not UserModel.find_by_username(data['username']):
                user.username = data['username']
                user.email = data['email']
                db.session.commit()
                return {'message': 'Your account has been updated'}, 201
            return {'message': "New username has been taken!"}, 400
        return {'message': f'User {username} not found'}

    @jwt_required()
    def delete(self):
        """Delete current username"""
        username = current_identity
        user = username.delete_from_db()
        return {"message": "Your username has been deleted."}


class UserRegisteration(Resource):
    def post(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help="This field cannot be blank!")
        parser.add_argument('password', required=True, help="This field cannot be blank!")
        data = parser.parse_args()

        user = UserModel(username, data['email'], data['password'])
        try:
            user.save_to_db()
            return user.to_dict(), 201
        except IntegrityError:
            db.session.rollback()
            return {'error': f'Username {username} is already taken'}, 400


class UsersList(Resource):
    def get(self):
        return UserModel.return_all()
