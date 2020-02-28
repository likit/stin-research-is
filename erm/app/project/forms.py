from app import db
from flask_wtf import FlaskForm
from wtforms_alchemy import (model_form_factory, QuerySelectField)
from wtforms.widgets import Select
from .models import ProjectRecord, Application, ProjectMember
from app.main.models import User


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class ProjectRecordForm(ModelForm):
    class Meta:
        model = ProjectRecord
        exclude = ['approved_at', 'created_at', 'updated_at']


class ApplicationForm(ModelForm):
    class Meta:
        model = Application


class ProjectMemberForm(ModelForm):
    class Meta:
        model = ProjectMember

    users = QuerySelectField('User',
                             query_factory=lambda: User.query.filter_by(role=2),
                             widget=Select())
