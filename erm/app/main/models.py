from app import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    email = db.Column('email', db.String(255), unique=True, nullable=False)
    __password_hash = db.Column('password_hash', db.String(255), nullable=False)
    is_activated = db.Column('is_activated', db.Boolean(), default=False)
    #TODO: role should not be nullable
    role = db.Column('role', db.Integer, default=2,
                     # info={'label': 'role', 'choices': [(1, 'admin'), (2, 'user')]},
                     )

    def __init__(self, email, password):
        self.email = email
        self.__password_hash = generate_password_hash(password)

    def __str__(self):
        return self.email

    @property
    def fullname_thai(self):
        if self.profile:
            if self.profile.firstname_th and self.profile.lastname_th:
                return self.profile.fullname_th
            else:
                return self.email
        else:
            return self.email

    @property
    def password(self):
        raise ValueError('Password attribute is not accessible.')

    def check_password(self, password):
        return check_password_hash(self.__password_hash, password)

    @password.setter
    def password(self, new_password):
        self.__password_hash = generate_password_hash(new_password)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return self.is_activated

    @property
    def is_anonymous(self):
        return False

    def get_id(self):
        return str(self.id)

    @property
    def publications(self):
        pubs = [authored.pub for authored in self.authoreds]
        if pubs:
            return sorted(pubs, key=lambda x: x.pub_date, reverse=True)
        else:
            return pubs


class MailInfo(db.Model):
    __tablename__ = 'mail_info'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    signature = db.Column('signature', db.Text())

