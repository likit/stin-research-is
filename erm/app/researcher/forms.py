from app import db
from flask_wtf import FlaskForm
from wtforms_alchemy import (model_form_factory, QuerySelectField)
from wtforms.widgets import Select, ListWidget, CheckboxInput
from wtforms.fields import SelectMultipleField
from .models import *


BaseModelForm = model_form_factory(FlaskForm)


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


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


class IntlConferenceSupportForm(ModelForm):
    class Meta:
        model = IntlConferenceSupport
    qualifications = [(c, c) for c in
                      ('บุคลากรสถาบันฯและไม่อยู่ระหว่างลาศึกษา/ไปปฏิบัติงานเพื่อเพิ่มพูนความรู้',
                       'ปฎิบัติงานในสถาบันมาแล้วไม่น้อยกว่า 1 ปีและไม่อยู่ในระหว่างการลาศึกษาเต็มเวลา',
                       'ยังไม่เคยขอรับความสนับสนุน / เคยขอรับการสนับสนุนและตีพิมพ์เผยแพร่งานตามประกาศแล้ว',
                       'เป็นผู้เขียนชื่อแรกและหรือผู้รับผิดชอบหลัก')]
    qualification_select = MultiCheckboxField('คุณสมบัติของผู้ขอรับการสนับสนุนตามประกาศฯ',
                                              choices=qualifications)


class DevelopmentTypeForm(ModelForm):
    class Meta:
        model = DevelopmentType


class DevelopmentCategoryForm(ModelForm):
    class Meta:
        model = DevelopmentCategory
