from app import create_app
from flask_admin.contrib.sqla import ModelView
from app import admin, db
from app.main.models import User
from app.researcher.models import Profile, Program, Department, Education
from app.project.models import *
from flask_admin.contrib.sqla import ModelView


app = create_app()

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Profile, db.session))
admin.add_view(ModelView(Program, db.session))
admin.add_view(ModelView(Department, db.session))


class EducationModelView(ModelView):
    form_choices = {
        'degree': [('bachelor', 'bachelor'), ('master', 'master'), ('doctorate', 'doctorate')]
    }

admin.add_view(EducationModelView(Education, db.session))

class ProjectMemberModelView(ModelView):
    form_choices = {
        'role': [('head', 'Head'), ('researcher', 'Researcher'), ('coordinator', 'Coordinator')]
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
        'status': [('draft', 'Draft'), ('submitted', 'Submitted'),
                   ('revising', 'Revising'), ('approved', 'Approved')]
    }


admin.add_view(ProjectRecordModelView(ProjectRecord, db.session))
admin.add_view(ProjectMemberModelView(ProjectMember, db.session))
admin.add_view(ModelView(Category, db.session))
admin.add_view(ModelView(SubCategory, db.session))
