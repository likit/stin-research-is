from app import db
from app.main.models import User


class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    user_id = db.Column('user_id', db.ForeignKey('users.id'))
    user = db.relationship(User)
    role = db.Column('role', db.String(),
                     info={
                         'choices': [(i, i) for i in ['PI', 'co-PI', 'Coordinator', 'Researcher']],
                         'label': 'Role'
                     })
    project = db.relationship('ProjectRecord', backref=db.backref('members'))

    def __str__(self):
        return self.role


class ProjectRecord(db.Model):
    __tablename__ = 'projects'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title_th = db.Column('title_th', db.String(), info={'label': 'Title Thai'})
    subtitle_th = db.Column('subtitle_th', db.String(), info={'label': 'Subtitle Thai'})
    title_en = db.Column('title_en', db.String(), info={'label': 'Title English'})
    subtitle_en = db.Column('subtitle_en', db.String(), info={'label': 'Subtitle English'})
    objective = db.Column('objective', db.Text(), info={'label': 'Objective'})
    abstract = db.Column('abstract', db.Text(), info={'label': 'Abstract'})
    intro = db.Column('introduction', db.Text(), info={'label': 'Introduction'})
    method = db.Column('method', db.Text(), info={'label': 'Method'})
    status = db.Column('status', db.String(),
                       info={'label': 'Status',
                             'choices': [(i, i) for i in ['draft', 'concept', 'full',
                                                         'submitted', 'revising', 'approved',
                                                         'rejected', 'finished']]})
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    updated_at = db.Column('updated_at', db.DateTime(timezone=True))
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    approved_at = db.Column('approved_at', db.DateTime(timezone=True))
    denied_at = db.Column('denied_at', db.DateTime(timezone=True))
    #TODO: add cascading and nullable=False
    creator_id = db.Column('creator_id', db.ForeignKey('users.id'))
    creator = db.relationship('User', backref=db.backref('projects'), info={'label': 'Creator'})

    def __str__(self):
        return self.title_th[:50]


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    category = db.Column('category', db.String(), nullable=False, unique=True)

    def __str__(self):
        return '{}'.format(self.category)


class SubCategory(db.Model):
    __tablename__ = 'subcategories'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    category = db.Column('category', db.String(), nullable=False, unique=True)
    parent_id = db.Column('parent_id', db.ForeignKey('categories.id'))
    parent = db.relationship(Category, backref=db.backref('subcategories'))
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    project = db.relationship(ProjectRecord, backref=db.backref('subcategories'))

    def __str__(self):
        return '{} ({})'.format(self.category, self.parent)


class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    org = db.Column('organization', db.String(), nullable=False, info={'label': 'Organization'})
    detail = db.Column('detail', db.Text(), info={'label': 'Detail'})
    date = db.Column('date', db.Date(), info={'label': 'Date'})
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    project = db.relationship(ProjectRecord, backref=db.backref('applications'))
