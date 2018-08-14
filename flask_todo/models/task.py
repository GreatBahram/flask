from datetime import datetime

from flask_todo import db, bcrypt

DATE_FMT = '%d/%m/%Y %H:%M:%S'


class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    note = db.Column(db.String(80))
    creation_date = db.Column(db.DateTime, nullable=False, default=datetime.now)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)

    def __init__(self, username, email, password):
        self.name = name
        self.note = note
        self.password = password
        self.creation_date = datetime.now()

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'note': self.note,
            'creation_date': self.creation_date.strftime(DATE_FMT),
            'due_date': self.due_date.strftime(DATE_FMT) if self.due_date else None,
            'completed': self.completed,
            'profile_id': self.profile_id
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def __repr__(self):
        return f"<Task: {self.name}>"

