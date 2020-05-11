from app import create_app
from pytz import timezone
from flask_admin.contrib.sqla import ModelView
from app import admin, db
from app.main.models import User
from app.researcher.models import Profile, Program, Department, Education
from app.project.models import *
from flask_admin.contrib.sqla import ModelView


app = create_app()

@app.template_filter("localdatetime")
def local_datetime(dt):
    bangkok = timezone('Asia/Bangkok')
    datetime_format = '%d/%m/%Y %H:%M'
    return dt.astimezone(bangkok).strftime(datetime_format)


@app.template_filter("localdate")
def local_datetime(dt):
    bangkok = timezone('Asia/Bangkok')
    datetime_format = '%d/%m/%Y'
    return dt.strftime(datetime_format)


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Profile, db.session, category='Researcher'))
admin.add_view(ModelView(Program, db.session, category='Researcher'))
admin.add_view(ModelView(Department, db.session, category='Researcher'))



class EducationModelView(ModelView):
    form_choices = {
        'degree': [('Bachelor', 'Bachelor'), ('Master', 'Master'), ('Doctorate', 'Doctorate')]
    }

admin.add_view(EducationModelView(Education, db.session, category='Researcher'))

class ProjectMemberModelView(ModelView):
    form_choices = {
        'role': [('PI', 'PI'),
                 ('co-PI', 'co-PI'),
                 ('Researcher', 'Researcher'),
                 ('Coordinator', 'Coordinator'),
                 ]
    }


class ProjectRecordModelView(ModelView):
    can_view_details = True
    form_widget_args = {
        'intro': {
            'rows': 10,
        },
        'abstract': {
            'rows': 10
        },
        'method': {
            'rows': 10
        },
        'objective': {
            'rows': 10
        },
    }
    form_choices = {
        'status': [('draft', 'draft'), ('submitted', 'submitted'),
                   ('concept', 'concept'), ('full', 'full',),
                   ('revising', 'revising'),
                   ('rejected', 'rejected'),
                   ('finished', 'finished')]
    }


admin.add_view(ProjectRecordModelView(ProjectRecord, db.session, category='Project'))
admin.add_view(ProjectMemberModelView(ProjectMember, db.session, category='Project'))
admin.add_view(ModelView(Category, db.session, category='Project'))
admin.add_view(ModelView(SubCategory, db.session, category='Project'))
admin.add_view(ModelView(Application, db.session, category='Project'))
admin.add_view(ModelView(ProjectReviewerGroup, db.session, category='Project'))
admin.add_view(ModelView(ProjectReviewer, db.session, category='Project'))
admin.add_view(ModelView(ProjectReviewRecord, db.session, category='Project'))
admin.add_view(ModelView(ProjectPublicationJournal, db.session, category='Project'))
admin.add_view(ModelView(ProjectPublication, db.session, category='Project'))
admin.add_view(ModelView(ProjectPublicationAuthor, db.session, category='Project'))
admin.add_view(ModelView(ProjectLanguageEditingSupport, db.session, category='Project'))
admin.add_view(ModelView(ProjectMilestone, db.session, category='Project'))
admin.add_view(ModelView(ProjectBudgetCategory, db.session, category='Project'))
admin.add_view(ModelView(ProjectBudgetSubCategory, db.session, category='Project'))
admin.add_view(ModelView(ProjectBudgetItem, db.session, category='Project'))
