from app import db
from flask_wtf import FlaskForm
from wtforms_alchemy import (model_form_factory, QuerySelectField)
from wtforms_components import DateTimeField
from wtforms.widgets import Select, ListWidget, CheckboxInput
from wtforms.fields import SelectMultipleField, FileField, SelectField
from wtforms.validators import Optional, InputRequired
from .models import *
from app.main.models import User


class MultiCheckboxField(SelectMultipleField):
    widget = ListWidget(prefix_label=False)
    option_widget = CheckboxInput()


BaseModelForm = model_form_factory(FlaskForm)


class ModelForm(BaseModelForm):
    @classmethod
    def get_session(self):
        return db.session


class ProjectRecordForm(ModelForm):
    class Meta:
        model = ProjectRecord
        exclude = ['approved_at', 'created_at', 'updated_at']

    parent = QuerySelectField(ParentProjectRecord,
                              query_factory=lambda: ParentProjectRecord.query.all(),
                              allow_blank=True,
                              blank_text='โครงการเดี่ยว',
                              widget=Select())
    fund_source = QuerySelectField(ProjectFundSource,
                                   query_factory=lambda: ProjectFundSource.query.all(),
                                   widget=Select())
    contract_upload = FileField('Upload เอกสารสัญญา')
    final_report_upload = FileField('Upload รายงานฉบับสมบูรณ์')


class ApplicationForm(ModelForm):
    class Meta:
        model = Application


class ProjectMemberForm(ModelForm):
    class Meta:
        model = ProjectMember

    users = QuerySelectField('User',
                             query_factory=lambda: sorted([u for u in User.query.filter_by(role=2)],
                                                          key=lambda x: x.fullname_thai),
                             get_label='fullname_thai',
                             allow_blank=True,
                             blank_text='กรุณาเลือกนักวิจัย',
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

    qual_choices = [(i, i) for i in
                    ('บุคลากรของสถาบันฯ ซึ่งไม่อยู่ในระหว่างลาศึกษาต่อ/ไปปฏิบัติงานต่างประเทศ',
                     'เป็นผู้เขียนชื่อแรกหรือผู้รับผิดชอบบทความ',
                     'มีต้นฉบับบทความและได้รับการตีพิมพ์ในวารสารวิชาการระดับนานาชาติที่ปรากฏในฐานข้อมูล ISI (SCI/SSCI/A & HCI) หรือฐานข้อมูล SCOPUS'
                     )]
    qualification_select = MultiCheckboxField('คุณสมบัติของผู้ขอรับการสนับสนุนตามประกาศ', choices=qual_choices)
    criteria = [(i, i) for i in
                (
                "เป็นผลงานที่ได้รับการตีพิมพ์ในวารสารวิชาการระดับนานาชาติที่อยู่ในฐานข้อมูล ISI (SCI/SSCI/A&HCI), Scopus",
                "เป็นผลงานที่ยังไม่เคยขอรับเงินสนับสนุนการตรวจคุณภาพ/การตรวจทานภาษาของต้นฉบับ",
                "เป็นผลงานที่ตีพิมพ์ไม่เกิน 6 เดือน นับตั้งแต่วันที่ได้รับการสนับสนุน",
                "ไม่เป็นผลงานที่ได้รับเงินสนับสนุนจากวารสารที่ลงตีพิมพ์หรือแหล่งทุนอื่น หรือแหล่งทุนสนับสนุนการวิจัยซึ่งระบุไว้ในโครงการวิจัยแล้ว")
                ]
    criteria_select = MultiCheckboxField('เกณฑ์การให้เงินสนับสนุนการตรวจคุณภาพและการตรวจทานภาษาของต้นฉบับ',
                                         choices=criteria)
    request_select = MultiCheckboxField('การขอรับเงินสนับสนุน',
                                        choices=[(i, i) for i in
                                                 (
                                                 'การตรวจคุณภาพต้นฉบับบทความ (Manuscript) จ่ายเรื่องละไม่เกิน 5,000 บาท',
                                                 'การตรวจทานภาษาอังกฤษต้นฉบับบทความ (Manuscript) คำละ 1 บาท จ่ายเรื่องละไม่เกิน 5,000 บาท')])
    docs_select = MultiCheckboxField('หลักฐานประกอบการขอรับเงินสนับสนุน',
                                     choices=[(i, i) for i in
                                              (
                                              'หลักฐานการชำระเงินโดยต้องระบุชื่อผู้รับการสนับสนุนเช่น ใบเสร็จรับเงิน ใบแจ้งหนี้บัตรเครดิต ชื่อบทความ หลักฐานการโอนเงิน (ฉบับจริง) หากเป็นสำเนาต้องรับรองสำเนาถุกต้องและลงชื่อกำกับ',
                                              'ใบสำคัญรับเงินจากผู้ทรงคุณวุฒิพร้อมระบุลักษณะการตรวจ (ตรวจทานต้นฉบับ/ตรวจทานภาษาอังกฤษ) ชื่อบทความและจำนวนค่า พร้อมลงนามกำกับ',
                                              'สำเนาบัตรประชาชนของผู้ทรงคุณวุฒิ',
                                              'สำเนาบทความที่ได้รับการตีพิมพ์พร้อมรายละเอียดของวารสารที่มีชื่อปรากฏในฐานข้อมูล (SCI/SSCI/A&HCI) หรือ Scopus',
                                              )])


class ProjectPublishedRewardForm(ModelForm):
    class Meta:
        model = ProjectPublishedReward
        field_args = {'reward': {'validators': [Optional()]},
                      'apc': {'validators': [Optional()]}
                      }

    qualifications = [(c, c) for c in
                      ('บุคลากรสถาบันฯและไม่อยู่ระหว่างลาศึกษา/ไปปฏิบัติงานเพื่อเพิ่มพูนความรู้',
                       'เป็นผู้ประพันธ์ชื่อแรก (first author)',
                       'เป็นผู้รับผิดชอบบทความหลัก (corresponding author) กรณีนี้ต้องแนบใบยินยอมจากผู้เขียนชื่อแรกมาด้วย',
                       'เป็นผู้มีส่วนร่วมเท่ากัน (equal contribution)',
                       'บทความนี้ไม่มีการตีพิมพ์ซ้ำซ้อน',
                       'บทความนี้ไม่เคยขอหรืออยู่ระหว่างการขอรับเงินสนับสนุนการตีพิมพ์จากแหล่งทุนอื่น')]
    qualification_select = MultiCheckboxField(
        'คุณสมบัติของผู้ขอรับเงินสนับสนุนและรางวัลการตีพิมพ์ผลงานวิชาการ', choices=qualifications)


class ProjectPublicationAuthorForm(ModelForm):
    class Meta:
        model = ProjectPublicationAuthor

    users = QuerySelectField(User,
                             query_factory=lambda: sorted([u for u in User.query.filter_by(role=2)],
                                                          key=lambda x: x.fullname_thai),
                             get_label=lambda x: x.profile.fullname_th,
                             widget=Select(), validators=[Optional()])


class ProjectGanttActivityForm(ModelForm):
    class Meta:
        model = ProjectGanttActivity


class ProjectOverallGanttActivityForm(ModelForm):
    class Meta:
        model = ProjectOverallGanttActivity


class ProjectBudgetItemForm(ModelForm):
    class Meta:
        model = ProjectBudgetItem

    sub_category = QuerySelectField(ProjectBudgetSubCategory,
                                    query_factory=lambda: ProjectBudgetSubCategory.query.all(),
                                    widget=Select())


class ProjectBudgetItemOverallForm(ModelForm):
    class Meta:
        model = ProjectBudgetItemOverall

    sub_category = QuerySelectField(ProjectBudgetSubCategory,
                                    query_factory=lambda: ProjectBudgetSubCategory.query.all(),
                                    widget=Select())


class ProjectSummaryForm(ModelForm):
    class Meta:
        model = ProjectSummary


class ParentProjectRecordForm(ModelForm):
    class Meta:
        model = ParentProjectRecord


class ProjectProposalDevelopmentSupportForm(ModelForm):
    class Meta:
        model = ProjectProposalDevelopmentSupport

    qualifications = [(c, c) for c in
                      ('บุคลากรสถาบันฯและไม่อยู่ระหว่างลาศึกษา/ไปปฏิบัติงานเพื่อเพิ่มพูนความรู้',
                       'เป็นหัวหน้าโครงการวิจัย / ผู้อำนวยการแผนงานวิจัย โดยระบุชื่อหน่วยงานของสถาบันอย่างชัดเจน')]
    qualification_select = MultiCheckboxField('คุณสมบัติของผู้ขอรับการสนับสนุนตามประกาศฯ',
                                              choices=qualifications)
    docs_select = MultiCheckboxField('หลักฐานประกอบการขอรับเงินสนับสนุน',
                                     choices=[(i, i) for i in
                                              (
                                              'หลักฐานการชำระเงินโดยต้องระบุชื่อผู้รับการสนับสนุนเช่น ใบเสร็จรับเงิน หรือหลักฐานการโอนเงิน (ฉบับจริง) หากเป็นสำเนาต้องรับรองสำเนาถุกต้องและลงชื่อกำกับ',
                                              'ใบสำคัญรับเงินจากผู้ทรงคุณวุฒิพร้อมระบุลักษณะการตรวจ (ให้คำปรึกษาเพื่อพัฒนาโครงการวิจัยหรือแผนงานวิจัยและสถิติวิจัย) ต้องระบุชื่อโครงการวิจัยหรือแผนงานวิจัยพร้อมลงนามกำกับ',
                                              'สำเนาหนังสือรับรองจริยธรรมวิจัยในคน',
                                              'สำเนาโครงการวิจัยหรือแผนงานวิจัยที่ผ่านการพิจารณาจากคณะกรรมการจริยธรรมการวิจัยในคน',
                                              )])
    contract_upload = FileField('Upload เอกสารสัญญา')


class EthicRecordForm(ModelForm):
    file_upload = FileField('Upload เอกสาร')


class SupplementaryDocumentForm(ModelForm):
    class Meta:
        model = ProjectSupplementaryDocument

    file_upload = FileField('Upload เอกสาร')


class FileUploadForm(FlaskForm):
    file_type = SelectField('File',
                            choices=[('finance', 'ใบสรุปการใช้เงิน'),
                                     ('bookbank_cover', 'หน้าแรกสมุดบัญชี'),
                                     ('bookbank_last_page', 'หน้าสุดท้ายสมุดบัญชี')
                                     ])
    file_upload = FileField('Upload')
