from app.project.models import (ProjectReviewSendRecord,
                                ProjectReviewRecord,
                                ProjectEthicReviewRecord,
                                ProjectEthicReviewSendRecord)
from wsgi import db
from wtforms_alchemy import (model_form_factory, QuerySelectField)
from flask_wtf import FlaskForm


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class ProjectReviewSendRecordForm(BaseModelForm):
    class Meta:
        model = ProjectReviewSendRecord


class ProjectReviewRecordForm(BaseModelForm):
    class Meta:
        model = ProjectReviewRecord


class ProjectEthicReviewSendRecordForm(BaseModelForm):
    class Meta:
        model = ProjectEthicReviewSendRecord


class ProjectEthicReviewRecordForm(BaseModelForm):
    class Meta:
        model = ProjectEthicReviewRecord