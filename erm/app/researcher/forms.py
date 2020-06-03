from app import db
from flask_wtf import FlaskForm
from wtforms_alchemy import (model_form_factory, QuerySelectField)
from wtforms.fields import FileField
from wtforms.widgets import Select
from .models import Profile, Program, Education


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class ProgramForm(ModelForm):
    class Meta:
        model = Program


class ProfileForm(ModelForm):
    class Meta:
        model = Profile

    programs = QuerySelectField('Program',
                                query_factory=lambda: Program.query,
                                widget=Select())
    photo_upload = FileField('Photo Upload')


class EducationForm(ModelForm):
    class Meta:
        model = Education

