"""Entire flask app."""
from datetime import datetime
from flask import Flask, jsonify, request, Response
from flask_sqlalchemy import SQLAlchemy
from flask_httpauth import HTTPTokenAuth
from functools import wraps
import json
import os
from passlib.hash import pbkdf2_sha256 as hasher


INCOMING_DATE_FMT = '%d/%m/%Y %H:%M:%S'


def forbidden_response():
    """Return an HTTP response when the user is forbidden."""
    response = Response(
        mimetype="application/json",
        response=json.dumps({'error': 'You do not have permission to access this profile.'}),
        status=403
    )
    return response

@auth.verify_token
def verify_token(token):
    """Verify that the incoming request has the expected token."""
    if token:
        username = token.split(':')[0]
        profile = get_profile(username)
        return token == profile.token


def authenticate(response, profile):
    """Authenticate an outgoing response with the user's token."""
    token = f'{profile.username}:{profile.token}'
    response.set_cookie('auth_token', value=token)
    return response

@app.route('/api/v1/accounts/<username>/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def task_update(username, task_id):
    profile = get_profile(username)
    if profile:
        task = Task.query.get(task_id)
        if task in profile.tasks:
            if 'name' in request.form:
                task.name = request.form['name']
            if 'note' in request.form:
                task.note = request.form['note']
            if 'completed' in request.form:
                task.completed = request.form['completed']
            if 'due_date' in request.form:
                due_date = request.form['due_date']
                task.due_date = datetime.strptime(due_date, INCOMING_DATE_FMT) if due_date else None
            db.session.add(task)
            db.session.commit()
            output = {'username': username, 'task': task.to_dict()}
            response = Response(
                mimetype="application/json",
                response=json.dumps(output)
            )
            return authenticate(response, profile)
    return notfound_response()    


@app.route('/api/v1/accounts/<username>/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def task_delete(username, task_id):
    profile = get_profile(username)
    if profile:
        task = Task.query.get(task_id)
        if task in profile.tasks:
            db.session.delete(task)
            db.session.commit()
            output = {'username': username, 'msg': 'Deleted.'}
            response = Response(
                mimetype="application/json",
                response=json.dumps(output)
            )
            return authenticate(response, profile)
    return notfound_response()    
