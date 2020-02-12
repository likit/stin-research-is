from app import create_app
from flask_admin.contrib.sqla import ModelView
from app import admin, db
from app.main.models import User
from app.researcher.models import Profile, Program, Department, Education
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
