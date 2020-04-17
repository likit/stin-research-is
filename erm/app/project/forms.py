from app import db
from flask_wtf import FlaskForm
from wtforms_alchemy import (model_form_factory, QuerySelectField)
from wtforms_components import DateTimeField
from wtforms.widgets import Select
from wtforms.validators import Optional
from .models import *
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
                             get_label='fullname_thai',
                             widget=Select())


class ProjectFigureForm(ModelForm):
    class Meta:
        model = ProjectFigure


class ProjectMilestoneForm(ModelForm):
    class Meta:
        model = ProjectMilestone


class ProjectJournalForm(ModelForm):
    class Meta:
        model = ProjectPublicationJournal


class ProjectPublicationForm(ModelForm):
    class Meta:
        model = ProjectPublication
    journals = QuerySelectField(ProjectPublicationJournal,
                             query_factory=lambda: ProjectPublicationJournal.query.all(),
                             get_label=lambda x: x.name,
                             widget=Select())


class ProjectLanguageEditSupportForm(ModelForm):
    class Meta:
        model = ProjectLanguageEditingSupport


class ProjectPublicationAuthorForm(ModelForm):
    class Meta:
        model = ProjectPublicationAuthor
    users = QuerySelectField(User,
                             query_factory=lambda: User.query.filter_by(role=2),
                             get_label=lambda x: x.profile.fullname_th,
                             widget=Select(), validators=[Optional()])
