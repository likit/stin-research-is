from app import db
from flask_wtf import FlaskForm
from wtforms_alchemy import (model_form_factory, QuerySelectField)
from wtforms.widgets import Select
from .models import Profile, Program


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

