from app import db
from app.main.models import User


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name_th = db.Column('name_th', db.String(),
                        nullable=False, unique=True,
                        info={'label': 'TH Name'})
    name_en = db.Column('name_en', db.String(), unique=True,
                        info={'label': 'EN Name'})

    def __str__(self):
        return self.name_th


class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name_th = db.Column('name_th', db.String(), nullable=False, unique=True)
    name_en = db.Column('name_en', db.String(), unique=True)
    dept_id = db.Column('dept_id', db.ForeignKey('departments.id'))
    dept = db.relationship(Department, backref=db.backref('programs'))

    def __str__(self):
        return '{} {}'.format(self.name_th, self.dept)


class Education(db.Model):
    __tablename__ = 'educations'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    degree = db.Column('degree',
                       db.String(),
                       info={'choices': [(i, i) for i in ['Bachelor', 'Master', 'Doctorate']]},
                       nullable=False)
    degree_title = db.Column('degree_title', db.String())
    field = db.Column('field', db.String())
    program = db.Column('program', db.String())
    university = db.Column('university', db.String())
    year = db.Column('year', db.Integer, nullable=False)
    profile_id = db.Column('profile_id', db.ForeignKey('profiles.id'))
    profile = db.relationship('Profile', backref=db.backref('educations'))


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey('users.id'))
    user = db.relationship(User, backref=db.backref('profile', uselist=False))
    title_th = db.Column('title_th', db.String(), info={'label': 'Thai Title'})
    title_en = db.Column('title_en', db.String(), info={'label': 'English Title'})
    firstname_th = db.Column('firstname_th', db.String(), info={'label': 'Thai First Name'})
    lastname_th = db.Column('lastname_th', db.String(), info={'label': 'Thai Last Name'})
    firstname_en = db.Column('firstname_en', db.String(), info={'label': 'English First Name'})
    lastname_en = db.Column('lastname_en', db.String(), info={'label': 'English Last Name'})
    program_id = db.Column('program_id', db.ForeignKey('programs.id'))
    program = db.relationship(Program, backref=db.backref('researchers'))

    def __init__(self, user_id=None):
        self.user_id = user_id

    def __str__(self):
        return self.fullname_th

    @property
    def fullname_th(self):
        return '{} {}'.format(self.firstname_th, self.lastname_th)

    @property
    def fullname_en(self):
        return '{} {}'.format(self.firstname_en, self.lastname_en)

    @property
    def affiliation(self):
        return '{} {}'.format(self.program, self.program.department)
