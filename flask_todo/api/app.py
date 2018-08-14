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


def notfound_response():
    """Return an HTTP response when a nonexistant profile has been searched for."""
    response = Response(
        mimetype="application/json",
        response=json.dumps({'error': 'The profile does not exist'}),
        status=404
    )
    return response

def get_profile(username):
    """Check if the requested profile exists."""
    return Profile.query.filter_by(username=username).first()


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



@app.route('/api/v1/accounts/logout', methods=["GET"])
def logout():
    """Log a user out."""
    return jsonify({'msg': 'Logged out.'})




@app.route('/api/v1/accounts/<username>/tasks', methods=['GET'])
@auth.login_required
def task_list(username):
    """List all of the tasks for one user."""
    profile = get_profile(username)
    if profile:
        tasks = [task.to_dict() for task in profile.tasks.all()]
        output = {'username': username, 'tasks': tasks}
        response = Response(
            mimetype="application/json",
            response=json.dumps(output)
        )
        return authenticate(response, profile)
    return notfound_response()


@app.route('/api/v1/accounts/<username>/tasks', methods=['POST'])
@auth.login_required
def create_task(username):
    """List all of the tasks for one user."""
    profile = get_profile(username)
    if profile:
        task = Task(
            name=request.form['name'],
            note=request.form['note'],
            creation_date=datetime.now(),
            due_date=datetime.strptime(due_date, INCOMING_DATE_FMT) if due_date else None,
            completed=request.form['completed'],
            profile_id=profile.id,
        )
        db.session.add(task)
        db.session.commit()
        output = {'msg': 'posted'}
        response = Response(
            mimetype="application/json",
            response=json.dumps(output),
            status=201
        )
        return authenticate(response, profile)
    return notfound_response()


@app.route('/api/v1/accounts/<username>/tasks/<int:task_id>', methods=['GET'])
@auth.login_required
def task_detail(username, task_id):
    """Get the detail for one task if that task belongs to the provided user."""
    profile = get_profile(username)
    if profile:
        task = Task.query.get(task_id)
        if task in profile.tasks:
            output = {'username': username, 'task': task.to_dict()}
            response = Response(
                mimetype="application/json",
                response=json.dumps(output)
            )
            return authenticate(response, profile)
    return notfound_response()


@app.route('/api/v1/accounts/<username>/tasks/<int:task_id>', methods=['PUT'])
@auth.login_required
def task_update(username, task_id):
    """Update one task if that task belongs to the provided user."""
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
    """Delete one task if that task belongs to the provided user."""
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
