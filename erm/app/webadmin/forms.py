from app.project.models import (ProjectReviewSendRecord,
                                ProjectReviewRecord,
                                ProjectEthicReviewRecord,
                                ProjectEthicReviewSendRecord,
                                ProjectEthicRecord)
from wsgi import db
from wtforms_alchemy import (model_form_factory, QuerySelectField)
from wtforms.widgets import ListWidget, CheckboxInput
from wtforms.fields import SelectMultipleField, BooleanField, FileField
from wtforms.validators import DataRequired
from flask_wtf import FlaskForm

BaseModelForm = model_form_factory(FlaskForm)


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class ProjectReviewSendRecordForm(BaseModelForm):
    class Meta:
        model = ProjectReviewSendRecord


class ProjectReviewRecordAdminForm(BaseModelForm):
    class Meta:
        model = ProjectReviewRecord

    upload_file = FileField('Upload เอกสารแนบ')

    alignment_select = MultiCheckboxField('ความสอดคล้องกับยุทธศาสตร์หรือประเด็นการวิจัยหลักของสถาบัน',
                                          choices=[(i, i) for i in
                                                   ('การวิจัยด้านการพยาบาลผู้สูงอายุ',
                                                    'การวิจัยด้านภัยพิบัติและการจัดการสาธารณภัย'
                                                    'การวิจัยกลุ่มด้อยโอกาส',
                                                    'การวิจัยและการพัฒนานวัตกรรมทางการพยาบาล'
                                                    'การวิจัยด้านการศึกษาพยาบาล',
                                                    'การวิจัยในคลินิกและพัฒนาระบบบริการพยาบาล',
                                                    'อื่นๆ')])
    outcome_detail_select = MultiCheckboxField('รายการผลผลิตจากการวิจัย',
                                               choices=[(i, i) for i in
                                                        ('ตีพิมพ์ในวารสารระดับชาติ/นานาชาติ',
                                                         'เผยแพร่ระดับชาติ/นานาชาติ',
                                                         'จดข้อมูลลิขสิทธิ์/จดทะเบียนอนุสิทธิบัตร/จดทะเบียนสิทธิบัตร',
                                                         'อื่นๆ')])
    benefit_detail_select = MultiCheckboxField('รายการประโยชน์ที่คาดว่าจะได้รับ',
                                               choices=[(i, i) for i in
                                                        ('ประโยชน์เชิงสาธารณะ',
                                                         'ประโยชน์เชิงนโยบาย',
                                                         'ประโยชน์เชิงพานิชย์',
                                                         'ประโยชน์ทางอ้อมทางงานสร้างสรรค์',
                                                         'อื่นๆ')])


class ProjectReviewRecordForm(ProjectReviewRecordAdminForm):
    class Meta:
        model = ProjectReviewRecord

    confirm_submission = BooleanField('ยืนยันการส่งแบบฟอร์ม',
                                      validators=[DataRequired()])


class ProjectEthicReviewSendRecordForm(BaseModelForm):
    class Meta:
        model = ProjectEthicReviewSendRecord


class ProjectEthicReviewRecordForm(BaseModelForm):
    class Meta:
        model = ProjectEthicReviewRecord


class ProjectEthicRecordForm(BaseModelForm):
    class Meta:
        model = ProjectEthicRecord
