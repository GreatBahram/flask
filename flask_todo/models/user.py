from datetime import datetime

# local imports
from flask_todo import db, bcrypt

DATE_FMT = '%d/%m/%Y %H:%M:%S'


class UserModel(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(60), nullable=False, unique=True)
    email = db.Column(db.String(60), nullable=False)
    password_hash = db.Column(db.String(60), nullable=False)
    date_joined = db.Column(db.DateTime, nullable=False)
    tasks = db.relationship("TaskModel", backref='user',  cascade="all", lazy='dynamic')

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password
        self.date_joined = datetime.now()

    @property
    def password(self):
        """
        Prevent password from being accessed.
        """
        raise AttributeError('Password is not a readable attribute.')
    
    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def to_dict(self):
        """Get the object's properties as a dictionary."""

        return {
            "username": self.username,
            "email": self.email,
            "date_joined": self.date_joined.strftime(DATE_FMT),
            "tasks": [task.to_dict() for task in self.tasks.all()],
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_username(cls, username):
        return cls.query.filter_by(username=username).first()

    @classmethod
    def find_by_id(cls, user_id):
        return cls.query.filter_by(id=user_id).first()

    @classmethod
    def return_all(cls):
        def to_dict(user):
            return {'username': user.username,
                    'email': user.email,}
        return {'users': list(map(lambda x: to_dict(x), UserModel.query.all()))}

    def __repr__(self):
        return f"<User: {self.username}>"

