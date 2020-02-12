from app import db
from app.main.models import User


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey('users.id'))
    user = db.relationship(User, backref=db.backref('profile', uselist=False))
    title_th = db.Column('title_th', db.String())
    title_en = db.Column('title_en', db.String())
    firstname_th = db.Column('firstname_th', db.String())
    lastname_th = db.Column('lastname_th', db.String())
    firstname_en = db.Column('firstname_en', db.String())
    lastname_en = db.Column('lastname_en', db.String())

    def __init__(self, user_id):
        self.user_id = user_id

    @property
    def fullname_th(self):
        return '{} {}'.format(self.firstname_th, self.lastname_th)

    @property
    def fullname_en(self):
        return '{} {}'.format(self.firstname_en, self.lastname_en)
