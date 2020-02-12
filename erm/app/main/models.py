from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column('email', db.String(255), unique=True, nullable=False)
    password_hash = db.Column('password_hash', db.String(255), nullable=False)

    def __init__(self, email, password):
        self.email = email
        self.password_hash = generate_password_hash(password)

    def __str__(self):
        return self.email

    @property
    def password(self):
        raise ValueError('Password attribute is not accessible.')

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
