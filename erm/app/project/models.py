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


class ProjectFigure(db.Model):
    __tablename__ = 'project_figures'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    title = db.Column('title', db.String(), info={'label': 'Title'})
    desc = db.Column('desc', db.Text(), info={'label': 'Description'})
    fignum = db.Column('fignum', db.String(),
                       info={'label': 'Figure Number'})
    url = db.Column('url', db.String())
    project = db.relationship('ProjectRecord', backref=db.backref('figures'))


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
    prospected_journals = db.Column('prospected_journals', db.Text(),
                                    info={'label': 'Prospected Journals'})
    use_applications = db.Column('use_applications', db.Text(),
                                 info={'label': 'Uses or Applications'})
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    updated_at = db.Column('updated_at', db.DateTime(timezone=True))
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    approved_at = db.Column('approved_at', db.DateTime(timezone=True))
    denied_at = db.Column('denied_at', db.DateTime(timezone=True))
    #TODO: add cascading and nullable=False
    creator_id = db.Column('creator_id', db.ForeignKey('users.id'))
    creator = db.relationship('User', backref=db.backref('projects'), info={'label': 'Creator'})

    @property
    def reviewers(self):
        return set([review.reviewer for review in self.reviews])

    def __str__(self):
        return self.title_th[:50]


class ProjectRecordArchive(db.Model):
    __tablename__ = 'project_archives'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_record_id = db.Column('project_record_id', db.ForeignKey('projects.id'))
    archived_at = db.Column('archived_at', db.DateTime(timezone=True))
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
    prospected_journals = db.Column('prospected_journals', db.Text(),
                                    info={'label': 'Prospected Journals'})
    use_applications = db.Column('use_applications', db.Text(),
                                 info={'label': 'Uses or Applications'})
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    updated_at = db.Column('updated_at', db.DateTime(timezone=True))
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    approved_at = db.Column('approved_at', db.DateTime(timezone=True))
    denied_at = db.Column('denied_at', db.DateTime(timezone=True))
    #TODO: add cascading and nullable=False
    creator_id = db.Column('creator_id', db.ForeignKey('users.id'))
    project = db.relationship('ProjectRecord', backref=db.backref('archives'))
    members = db.Column('members', db.JSON())
    figures = db.Column('figures', db.JSON())
    milestones = db.Column('milestones', db.JSON())

    def __str__(self):
        return '[{}] {}'.format(self.id, self.title_th[:50])

    def __repr__(self):
        return '<Archive: project id={}; status={}>'.format(self.project_record_id, self.status)


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


class ProjectEthicRecord(db.Model):
    __tablename__ = 'project_ethics'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    status = db.Column('status', db.String(),
                       info={'label': 'Status',
                             'choices': [(i, i) for i in ['submitted', 'pending', 'reviewing',
                                                          'revising', 'approved', 'rejected',
                                                          ]]})
    project = db.relationship('ProjectRecord', backref=db.backref('ethics'))


class ProjectMilestone(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    deadline = db.Column('deadline', db.DateTime(timezone=True), info={'label': 'Deadline Date'})
    goal = db.Column('goal', db.String(), nullable=False, info={'label': 'Goal/Task/Requirement'})
    detail = db.Column('detail', db.Text(), info={'label': 'Detail'})
    status = db.Column('status', db.String(),
                       info={'label': 'Status',
                             'choices': [(i, i) for i in ['started', 'ended', 'delayed']]})
    project = db.relationship('ProjectRecord', backref=db.backref('milestones'))


reviewer_groups = db.Table('reviewer_groups',
    db.Column('group_id', db.Integer, db.ForeignKey('project_reviewer_groups.id'), primary_key=True),
    db.Column('reviewer_id', db.Integer, db.ForeignKey('project_reviewers.id'), primary_key=True)
)


class ProjectReviewerGroup(db.Model):
    __tablename__ = 'project_reviewer_groups'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title = db.Column('title', db.String(), nullable=False)

    def __str__(self):
        return self.title


class ProjectReviewer(db.Model):
    __tablename__ = 'project_reviewers'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    academic_title = db.Column('academic_title', db.String())
    firstname = db.Column('firstname', db.String(), nullable=False)
    lastname = db.Column('lastname', db.String(), nullable=False)
    email = db.Column('email', db.String(), nullable=False)
    affiliation = db.Column('affiliation', db.String())
    user_id = db.Column('user_id', db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('reviewer', uselist=False))
    groups = db.relationship('ProjectReviewerGroup',
                             secondary=reviewer_groups,
                             lazy='subquery',
                             backref=db.backref('reviewers'))

    @property
    def fullname(self):
        return '{} {}'.format(self.firstname, self.lastname)


class ProjectReviewRecord(db.Model):
    __tablename__ = 'project_review_records'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    reviewer_id = db.Column('reviewer_id', db.ForeignKey('project_reviewers.id'))
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    comment = db.Column('comment', db.Text())
    status = db.Column('status', db.String(), default='pending',
                       info={
                           'label': 'decision',
                           'choices': [(i, i) for i in
                                         ('pending', 'revise',
                                          'approved', 'rejected')]
                             },
                       )
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    reviewer = db.relationship('ProjectReviewer', backref=db.backref('records'))
    project = db.relationship('ProjectRecord', backref=db.backref('reviews'))


class ProjectReviewSendRecord(db.Model):
    __tablename__ = 'project_review_send_records'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    review_id = db.Column('reviewer_id', db.ForeignKey('project_reviewers.id'))
    sent_at = db.Column('sent_at', db.DateTime(timezone=True))
    title = db.Column('title', db.String(), nullable=False)
    message = db.Column('message', db.Text())
    deadline = db.Column('deadline', db.DateTime(timezone=True))
    review = db.relationship('ProjectReviewer', backref=db.backref('send_records'))

