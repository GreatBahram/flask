from flask_todo import db, bcrypt

DATE_FMT = '%d/%m/%Y %H:%M:%S'


class TaskModel(db.Model):
    __tablename__ = 'tasks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Unicode, nullable=False)
    note = db.Column(db.Unicode)
    creation_date = db.Column(db.DateTime, nullable=False)
    due_date = db.Column(db.DateTime)
    completed = db.Column(db.Boolean, default=False)
    #user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    #user = db.relationship("UserModel", back_populates='tasks')

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

    def __repr__(self):
        return f"<Task: {self.name}>"

