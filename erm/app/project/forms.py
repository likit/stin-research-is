from app import db
from flask_wtf import FlaskForm
from wtforms_alchemy import (model_form_factory, QuerySelectField)
from wtforms.widgets import Select
from .models import ProjectRecord


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class ProjectRecordForm(ModelForm):
    class Meta:
        model = ProjectRecord
        exclude = ['approved_at', 'created_at', 'updated_at']

