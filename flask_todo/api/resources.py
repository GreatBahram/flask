# third-party imports
from flask import jsonify
from flask_restful import Resource, reqparse
from flask_jwt import jwt_required, current_identity

from flask_todo.models.user import UserModel
from flask_todo import db


class UsersList(Resource):
    def get(self):
        return UserModel.return_all()

class User(Resource):
    @jwt_required()
    def get(self, username):
        """Get the detail for an individual profile."""
        user = UserModel.query.filter_by(username=username).first()
        if user:
            return user.to_dict()
        return {"message": "User not found"}

    def post(self, username):
        parser = reqparse.RequestParser()
        parser.add_argument('email', required=True, help="This field cannot be blank!")
        parser.add_argument('username', required=True, help="This field cannot be blank!")
        parser.add_argument('password', required=True, help="This field cannot be blank!")
        data = parser.parse_args()
        if UserModel.find_by_username(username):
            return {'error': f'Username {username} is already taken'}, 400

        user = UserModel(username, data['email'], data['password'])
        user.save_to_db()
        return user.to_dict(), 201

    @jwt_required
    def put(self, username):
        """Add a new user profile if it doesn't already exist."""
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
    def delete(self, username):
        """Delete current username"""
        #UserModel.delete_by_username(current_identity.username)
        pass
