from app import db
from app.main.models import User


class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    user_id = db.Column('user_id', db.ForeignKey('users.id'))
    user = db.relationship(User)
    role = db.Column('role', db.String())
    project = db.relationship('ProjectRecord', backref=db.backref('members'))



class ProjectRecord(db.Model):
    __tablename__ = 'projects'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title_th = db.Column('title_th', db.String())
    subtitle_th = db.Column('subtitle_th', db.String())
    title_en = db.Column('title_en', db.String())
    subtitle_en = db.Column('subtitle_en', db.String())
    objective = db.Column('objective', db.Text())
    abstract = db.Column('abstract', db.Text())
    intro = db.Column('introduction', db.Text())
    method = db.Column('method', db.Text())
    status = db.Column('status', db.String())

    def __str__(self):
        return self.title_th[:50]
