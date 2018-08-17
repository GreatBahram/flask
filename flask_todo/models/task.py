from datetime import datetime

from flask_todo import db

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

    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'note': self.note,
            'creation_date': self.creation_date.strftime(DATE_FMT),
            'due_date': self.due_date.strftime(DATE_FMT) if self.due_date else None,
            'completed': self.completed,
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_id(cls, task_id):
        return cls.query.filter_by(id=task_id).first()

    def __repr__(self):
        return f"<Task: {self.name}>"
