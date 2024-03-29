import sqlalchemy
from sqlalchemy_continuum import make_versioned
from sqlalchemy_continuum.plugins import FlaskPlugin

from app import db
from app.main.models import User
from datetime import datetime

make_versioned(plugins=[FlaskPlugin()])


class ProjectMember(db.Model):
    __tablename__ = 'project_members'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    user_id = db.Column('user_id', db.ForeignKey('users.id'))
    user = db.relationship(User)
    role = db.Column('role', db.String(),
                     info={
                         'choices': [(i, i) for i in ['PI', 'co-PI', 'Coordinator', 'Researcher', 'Research Assistant']],
                         'label': 'Role'
                     })
    project = db.relationship('ProjectRecord', backref=db.backref('members'))
    title = db.Column('title', db.String(), info={'label': 'คำนำหน้า'})
    firstname = db.Column('firstname', db.String(), info={'label': 'ชื่อ'})
    lastname = db.Column('lastname', db.String(), info={'label': 'นามสกุล'})
    affil = db.Column('affiliation', db.String(), info={'label': 'สังกัด'})
    email = db.Column('email', db.String(), info={'label': 'E-mail'})
    contribution = db.Column('contribution', db.Numeric(), info={'label': 'สัดส่วนในผลงานวิจัย'})

    def __str__(self):
        return self.role

    @property
    def fullname(self):
        return '{}{} {}'.format(self.title, self.firstname, self.lastname)


class ProjectFigure(db.Model):
    __tablename__ = 'project_figures'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    title = db.Column('title', db.String(), info={'label': 'Title'})
    desc = db.Column('desc', db.Text(), info={'label': 'Description'})
    fignum = db.Column('fignum', db.String(),
                       info={'label': 'Figure Number'})
    url = db.Column('url', db.String())
    project = db.relationship('ProjectRecord', backref=db.backref('figures'))


class ParentProjectRecord(db.Model):
    __tablename__ = 'parent_projects'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title_th = db.Column('title_th', db.String(), info={'label': 'Title Thai'})
    subtitle_th = db.Column('subtitle_th', db.String(), info={'label': 'Subtitle Thai'})
    title_en = db.Column('title_en', db.String(), info={'label': 'Title English'})
    subtitle_en = db.Column('subtitle_en', db.String(), info={'label': 'Subtitle English'})
    created_at = db.Column('created_at', db.DateTime())
    creator_id = db.Column('creator_id', db.ForeignKey('users.id'))
    created_by = db.relationship(User, backref=db.backref('created_parent_projects'))

    def __str__(self):
        return self.title_th


class ProjectFundSource(db.Model):
    __tablename__ = 'project_fund_sources'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(), nullable=False)
    from_ = db.Column('from', db.String(), info={'label': 'ที่มาของทุน',
                                                 'choices': [(c, c) for c in
                                                             ('ภายใน', 'ภายนอก')]})
    def __str__(self):
        return self.name


class ProjectRecord(db.Model):
    __tablename__ = 'projects'
    __versioned__ = {
        'exclude': ['submitted_at', 'approved_at', 'close_requested_at',
                    'denied_at', 'contract_no', 'contract_url',
                    'final_report_url', 'finance_summary_file_url', 'book_bank_cover_file_url',
                    'book_bank_last_page_file_url', 'status', 'updated_at']
    }
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    fund_source_id = db.Column('fund_source_id',
                                       db.ForeignKey('project_fund_sources.id'))
    fund_source = db.relationship(ProjectFundSource, backref=db.backref('projects'))
    title_th = db.Column('title_th', db.String(), info={'label': 'ชื่อภาษาไทย'})
    subtitle_th = db.Column('subtitle_th', db.String(), info={'label': 'ชื่อรองภาษาไทย'})
    title_en = db.Column('title_en', db.String(), info={'label': 'ชื่อภาษาอังกฤษ'})
    subtitle_en = db.Column('subtitle_en', db.String(), info={'label': 'ชื่อรองภาษาอังกฤษ'})
    parent_project_id = db.Column('parent_project_id',
                                  db.ForeignKey('parent_projects.id'),
                                  default=None)
    parent_project = db.relationship(ParentProjectRecord, backref=db.backref('children_projects'))
    objective = db.Column('objective', db.Text(), info={'label': 'วัตถุประสงค์ของโครงการวิจัย'})
    abstract = db.Column('abstract', db.Text(), info={'label': 'บทคัดย่อ'})
    intro = db.Column('introduction', db.Text(), info={'label': 'ความสำคัญและที่มาของปัญหาที่ทำการวิจัย'})
    method = db.Column('method', db.Text(), info={'label': 'ระเบียบวิธีวิจัย'})
    research_type = db.Column('research_type', db.String(), info={'label': 'ประเภทงานวิจัย'})
    research_cluster = db.Column('research_cluster', db.String(), info={'label': 'สาขาวิชาการและกลุ่มที่ทำวิจัย'})
    keywords = db.Column('keywords', db.String(), info={'label': 'คำสำคัญของโครงการวิจัย'})
    scope = db.Column('scope', db.Text(), info={'label': 'ขอบเขตของโครงการวิจัย'})
    glossary = db.Column('glossary', db.Text(), info={'label': 'นิยามคำศัพท์'})
    conceptual_framework = db.Column('conceptual_framework', db.Text(),
                                     info={'label': 'ทฤษฎี สมมุติฐาน (ถ้ามี) กรอบแนวคิดของโครงการวิจัย'})
    literature_review = db.Column('literature_review', db.Text(),
                                     info={'label': 'การทบทวนวรรณกรรม/สารสนเทศที่เกี่ยวข้อง'})
    references = db.Column('references', db.Text(), info={'label': 'เอกสารอ้างอิง'})
    expected_benefit = db.Column('expected_benefit', db.Text(), info={'label': 'ประโยชน์ที่คาดว่าจะได้รับ'})
    status = db.Column('status', db.String(),
                       info={'label': 'สถานะโครงการ',
                             'choices': [(i, c) for i, c in [('draft', 'Draft'),
                                                          ('submitted', 'Submitted'),
                                                          ('revising', 'Revising'),
                                                          ('approved', 'Approved'),
                                                          ('rejected', 'Rejected'),
                                                          ('finish_pending', 'Finish Pending'),
                                                          ('finished', 'Finished'),
                                                          ('terminated', 'Terminated')
                                                         ]
                                        ]
                            })
    prospected_journals = db.Column('prospected_journals', db.Text(),
                                    info={'label': 'วารสารวิชาการที่คาดหวังจะส่งผลงานเข้าเผยแพร่'})
    use_applications = db.Column('use_applications', db.Text(),
                                 info={'label': 'การนำผลงานวิจัยไปใช้ประโยชน์'})
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    updated_at = db.Column('updated_at', db.DateTime(timezone=True))
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    approved_at = db.Column('approved_at', db.DateTime(timezone=True))
    close_requested_at = db.Column('close_requested_at', db.DateTime(timezone=True))
    closed_at = db.Column('closed_at', db.DateTime(timezone=True))
    denied_at = db.Column('denied_at', db.DateTime(timezone=True))
    #TODO: add cascading and nullable=False
    creator_id = db.Column('creator_id', db.ForeignKey('users.id'))
    creator = db.relationship('User', backref=db.backref('projects'), info={'label': 'ผู้บันทึกข้อมูล'})
    contract_no = db.Column('contract_no', db.String(), nullable=True, info={'label': 'หมายเลขสัญญา'})
    contract_url = db.Column('contract_url', db.String(), nullable=True)
    final_report_url = db.Column('final_report_url', db.String(), nullable=True, info={'label': 'รายงานฉบับสมบูรณ์'})
    finance_summary_file_url = db.Column('finance_summary_file_url', db.String(), nullable=True, info={'label': 'รายงานฉบับสมบูรณ์'})
    bookbank_cover_file_url = db.Column('bookbank_cover_file_url', db.String(), nullable=True, info={'label': 'รายงานฉบับสมบูรณ์'})
    bookbank_last_page_file_url = db.Column('bookbank_last_page_file_url', db.String(), nullable=True, info={'label': 'รายงานฉบับสมบูรณ์'})
    mentor = db.Column('mentor', db.String(), nullable=True, info={'label': 'ที่ปรึกษา'})

    @property
    def reviewers(self):
        return set([review.reviewer for review in self.reviews if review.reviewer is not None])

    @property
    def summarized_review_ready(self):
        review = [r for r in self.reviews if r.summarized]
        return len(review) > 0

    @property
    def ethic_reviewers(self):
        return set([review.reviewer for review in self.ethic_reviews])

    def get_ethic_status(self):
        if self.ethics:
            recent_request = self.ethics[0]
            return recent_request.status
        else:
            None

    @property
    def editable(self):
        return self.status == 'draft' or self.status == 'revising'

    @property
    def draft_mode(self):
        return self.status == 'draft'

    @property
    def approved(self):
        return self.status == 'approved'

    @property
    def finish_pending(self):
        return self.status == 'finish_pending'

    @property
    def finished(self):
        return self.status == 'finished'

    @property
    def revising(self):
        return self.status == 'revising'

    @property
    def submitted(self):
        return self.status == 'submitted'

    @property
    def rejected(self):
        return self.status == 'rejected'

    @property
    def terminated(self):
        return self.status == 'terminated'

    def __str__(self):
        return self.title_th[:50]


class ProjectRecordArchive(db.Model):
    __tablename__ = 'project_archives'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_record_id = db.Column('project_record_id', db.ForeignKey('projects.id'))
    archived_at = db.Column('archived_at', db.DateTime(timezone=True))
    title_th = db.Column('title_th', db.String(), info={'label': 'Title Thai'})
    subtitle_th = db.Column('subtitle_th', db.String(), info={'label': 'Subtitle Thai'})
    title_en = db.Column('title_en', db.String(), info={'label': 'Title English'})
    subtitle_en = db.Column('subtitle_en', db.String(), info={'label': 'Subtitle English'})
    objective = db.Column('objective', db.Text(), info={'label': 'Objective'})
    abstract = db.Column('abstract', db.Text(), info={'label': 'Abstract'})
    intro = db.Column('introduction', db.Text(), info={'label': 'Introduction'})
    method = db.Column('method', db.Text(), info={'label': 'Method'})
    status = db.Column('status', db.String(),
                       info={'label': 'Status',
                             'choices': [(i, i) for i in ['draft', 'concept', 'full',
                                                          'submitted', 'revising', 'approved',
                                                          'rejected', 'finished']]})
    prospected_journals = db.Column('prospected_journals', db.Text(),
                                    info={'label': 'Prospected Journals'})
    use_applications = db.Column('use_applications', db.Text(),
                                 info={'label': 'Uses or Applications'})
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    updated_at = db.Column('updated_at', db.DateTime(timezone=True))
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    approved_at = db.Column('approved_at', db.DateTime(timezone=True))
    denied_at = db.Column('denied_at', db.DateTime(timezone=True))
    #TODO: add cascading and nullable=False
    creator_id = db.Column('creator_id', db.ForeignKey('users.id'))
    project = db.relationship('ProjectRecord', backref=db.backref('archives'))
    members = db.Column('members', db.JSON())
    figures = db.Column('figures', db.JSON())
    milestones = db.Column('milestones', db.JSON())

    def __str__(self):
        return '[{}] {}'.format(self.id, self.title_th[:50])

    def __repr__(self):
        return '<Archive: project id={}; status={}>'.format(self.project_record_id, self.status)


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    category = db.Column('category', db.String(), nullable=False, unique=True)

    def __str__(self):
        return '{}'.format(self.category)


class SubCategory(db.Model):
    __tablename__ = 'subcategories'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    category = db.Column('category', db.String(), nullable=False, unique=True)
    parent_id = db.Column('parent_id', db.ForeignKey('categories.id'))
    parent = db.relationship(Category, backref=db.backref('subcategories'))
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    project = db.relationship(ProjectRecord, backref=db.backref('subcategories'))

    def __str__(self):
        return '{} ({})'.format(self.category, self.parent)


class Application(db.Model):
    __tablename__ = 'applications'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title = db.Column('title', db.String(), nullable=False, info={'label': 'ผลงานวิจัย/สร้างสรรค์เรื่อง'})
    research_tool = db.Column('research_tool', db.String(), nullable=False, info={'label': 'ชื่อเครื่องมือวิจัย'})
    finished_year = db.Column('finished_year', db.Integer, info={'label': 'แล้วเสร็จในปี'})
    date = db.Column('date', db.Date(), info={'label': 'วันที่'})
    public_how = db.Column('public_how', db.Text(), info={'label': 'ใช้ประโยชน์ในเชิงสาธารณะโดยการ'})
    public_outcome = db.Column('public_outcome', db.Text(), info={'label': 'ผลที่ได้'})
    policy_how = db.Column('policy_how', db.Text(), info={'label': 'ใช้ประโยชน์ในเชิงนโยบายโดยการ'})
    policy_outcome = db.Column('policy_outcome', db.Text(), info={'label': 'ผลที่ได้'})
    commercial_how = db.Column('commercial_how', db.Text(), info={'label': 'ใช้ประโยชน์ในเชิงพานิชย์โดยการ'})
    commercial_outcome = db.Column('commercial_outcome', db.Text(), info={'label': 'ผลที่ได้'})
    indirect_how = db.Column('indirect_how', db.Text(), info={'label': 'ใช้ประโยชน์ทางอ้อมของงานสร้างสรรค์'})
    indirect_outcome = db.Column('indirect_outcome', db.Text(), info={'label': 'ผลที่ได้'})
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    project = db.relationship(ProjectRecord, backref=db.backref('applications'))


class ProjectEthicRecord(db.Model):
    __tablename__ = 'project_ethics'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    updated_at = db.Column('updated_at', db.DateTime(timezone=True))
    upload_file_url = db.Column('upload_file_url', db.String())
    status = db.Column('status', db.String(),
                       info={'label': 'Status',
                             'choices': [(i, i) for i in ['submitted', 'pending', 'reviewing',
                                                          'revising', 'approved', 'rejected',
                                                          ]]})
    project = db.relationship('ProjectRecord', backref=db.backref('ethics'))

    @property
    def reviewers(self):
        return set([r.reviewer for r in self.reviews])


class ProjectMilestone(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    detail = db.Column('detail', db.Text(), info={'label': 'หากเปลี่ยนแปลงแผนงานโปรดระบุ'})
    plan = db.Column('plan', db.Text(), info={'label': 'การดำเนินงานในช่วงต่อไป'})
    related_activity = db.Column('related_activity', db.Text(),
                                 info={'label': 'กิจกรรมอื่นๆ ที่เกี่ยวข้อง'})
    obstacle = db.Column('obstacle', db.Text(), info={'label': 'อุปสรรคในการทำงานและแนวทางแก้ไข'})
    opinion = db.Column('opinion', db.Text(), info={'label': 'ความเห็นของผู้วิจัย'})
    file_url = db.Column('file_url', db.String())
    status = db.Column('status', db.String(),
                       info={'label': 'สถานะการดำเนินงาน',
                             'choices': [(i, i) for i in
                                         ('ดำเนินงานตามแผนที่ได้วางไว้ได้ทุกประการ',
                                          'ได้เปลี่ยนแปลงแผนงานที่ได้วางไว้ดังนี้'
                                          )]
                             })
    project = db.relationship('ProjectRecord', backref=db.backref('milestones'))
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    received_at = db.Column('received_at', db.DateTime(timezone=True))

    @property
    def is_editable(self):
        return False if self.submitted_at or self.received_at else True

    @property
    def gantt_activity_count(self):
        return len(self.gantt_activities)


GANTT_ACTIVITIES = [
    (1, 'พัฒนาโครงร่างการวิจัยและเครื่องมือการวิจัย'),
    (2, 'เสนอโครงร่างการวิจัยเพื่อขอรับการพิจารณาจริยธรรมฯ'),
    (3, 'เสนอขอรับทุนอุดหนุนการวิจัย'),
    (4, 'ผู้ทรงคุณวุฒิตรวจสอบและแก้ไข'),
    (5, 'ติดต่อประสานงานเพื่อขอเก็บข้อมูล'),
    (6, 'ดำเนินการเก็บรวบรวมข้อมูล'),
    (7, 'วิเคราะห์ผลการวิจัยและอภิปรายผล'),
    (8, 'จัดทำรายงานการวิจัยและเตรียมต้นฉบับตีพิมพ์งานวิจัย')
]

class ProjectGanttActivity(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    milestone_id = db.Column('milestone_id', db.ForeignKey('project_milestone.id'))
    milestone = db.relationship(ProjectMilestone, backref=db.backref('gantt_activities'))
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    detail = db.Column('detail', db.Text(), info={'label': 'รายละเอียด'})
    start_date = db.Column('start_date', db.Date(), info={'label': 'เริ่มต้น'})
    end_date = db.Column('end_date', db.Date(), info={'label': 'สิ้นสุด'})
    completion = db.Column('completion', db.Numeric(), info={'label': 'ร้อยละความสำเร็จ'}, default=100.0)
    dirty = db.Column('dirty', db.Boolean(), default=False)
    task_id = db.Column('task_id', db.Integer(),
                            info={
                                'label': 'กิจกรรม',
                                'choices': GANTT_ACTIVITIES
                            })


class ProjectOverallGanttActivity(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    detail = db.Column('detail', db.Text(), info={'label': 'รายละเอียด'})
    start_date = db.Column('start_date', db.Date(), info={'label': 'เริ่มต้น'})
    end_date = db.Column('end_date', db.Date(), info={'label': 'สิ้นสุด'})
    task_id = db.Column('task_id', db.Integer(),
                        info={
                            'label': 'กิจกรรม',
                            'choices': GANTT_ACTIVITIES
                        })
    project = db.relationship('ProjectRecord', backref=db.backref('gantt_activities'))


class ProjectSummary(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    milestone_id = db.Column('milestone_id', db.ForeignKey('project_milestone.id'))
    milestone = db.relationship(ProjectMilestone, backref=db.backref('summaries'))
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    edited_at = db.Column('edited_at', db.DateTime(timezone=True))
    activity = db.Column('activity', db.Unicode(), info={'label': 'กิจกรรมตามแผนงาน'})
    expected_outcome = db.Column('expected_outcome', db.Text(),
                                 info={'label': 'ผลผลิตที่ระบุไว้'})
    outcome = db.Column('outcome', db.Text(), info={'label': 'ผลผลิตที่เกิดขึ้นจริง'})


class ProjectBudgetCategory(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    category_id = db.Column('category_id', db.Integer())
    category = db.Column('category', db.String())

    def __str__(self):
        return self.category


class ProjectBudgetSubCategory(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    sub_category_id = db.Column('sub_category_id', db.Integer())
    sub_category = db.Column('sub_category', db.String())
    category_id = db.Column('category_id', db.ForeignKey('project_budget_category.id'))
    category = db.relationship(ProjectBudgetCategory, backref=db.backref('subcategories'))
    desc = db.Column('desc', db.String(255), nullable=True, info={
        'label': 'รายละเอียด'
    })

    def __str__(self):
        repr = '<{}> {}. {}'.format(self.category.category,
                                    self.sub_category_id, self.sub_category, self.desc)
        if self.desc:
            return '{} ({})'.format(repr, self.desc)
        else:
            return repr


class ProjectBudgetItem(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    sub_category_id = db.Column('sub_category_id', db.ForeignKey('project_budget_sub_category.id'))
    sub_category = db.relationship(ProjectBudgetSubCategory, backref=db.backref('items'))
    category_id = db.Column('category_id', db.ForeignKey('project_budget_category.id'))
    category = db.relationship(ProjectBudgetCategory, backref=db.backref('items'))
    item = db.Column('item', db.String(), info={'label': 'หมายเหตุ'})
    phase = db.Column('phase', db.String(),
                      info={'label': 'งวด',
                            'choices': [('1', 'งวดที่ 1'), ('2', 'งวดที่ 2'),
                                        ('3', 'งวดที่ 3'), ('4', 'งวดที่ 4')]})
    wage = db.Column('wage', db.Numeric(), default=0.0, info={'label': 'จำนวนเงิน (บาท)'})
    amount_spent = db.Column('amount_spent', db.Numeric(), default=0.0, info={'label': 'งบประมาณที่ใช้ไปแล้ว (บาท)'})
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    edited_at = db.Column('edited_at', db.DateTime(timezone=True))
    milestone_id = db.Column('milestone_id', db.ForeignKey('project_milestone.id'))
    milestone = db.relationship(ProjectMilestone, backref=db.backref('budget_items'))
    detail = db.Column('detail', db.Text(), info={'label': 'รายละเอียด'})
    file_name = db.Column('file_name', db.String(255), nullable=True)
    file_url = db.Column('file_url', db.Text(), nullable=True, info={'label': 'URL'})
    file_detail = db.Column('file_detail', db.Text(), nullable=True, info={'label': 'รายละเอียดเอกสารแนบ'})


class ProjectBudgetItemOverall(db.Model):
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    sub_category_id = db.Column('sub_category_id', db.ForeignKey('project_budget_sub_category.id'))
    sub_category = db.relationship(ProjectBudgetSubCategory, backref=db.backref('overall_items'))
    wage = db.Column('wage', db.Numeric(), default=0.0, info={'label': 'จำนวนเงิน (บาท)'})
    created_at = db.Column('created_at', db.DateTime(timezone=True))
    edited_at = db.Column('edited_at', db.DateTime(timezone=True))
    item = db.Column('item', db.String(), info={'label': 'หมายเหตุ'})
    phase = db.Column('phase', db.String(), default='0')
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    project = db.relationship('ProjectRecord', backref=db.backref('overall_budgets'))

    @property
    def category_ref(self):
        return '{}.{}'.format(self.sub_category.category.id, self.sub_category.id)


reviewer_groups = db.Table('reviewer_groups',
    db.Column('group_id', db.Integer, db.ForeignKey('project_reviewer_groups.id'), primary_key=True),
    db.Column('reviewer_id', db.Integer, db.ForeignKey('project_reviewers.id'), primary_key=True)
)


class ProjectReviewerGroup(db.Model):
    __tablename__ = 'project_reviewer_groups'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    title = db.Column('title', db.String(), nullable=False)

    def __str__(self):
        return self.title


class ProjectReviewer(db.Model):
    __tablename__ = 'project_reviewers'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    academic_title = db.Column('academic_title', db.String())
    firstname = db.Column('firstname', db.String(), nullable=False)
    lastname = db.Column('lastname', db.String(), nullable=False)
    email = db.Column('email', db.String(), nullable=False)
    affiliation = db.Column('affiliation', db.String())
    user_id = db.Column('user_id', db.ForeignKey('users.id'))
    user = db.relationship('User', backref=db.backref('reviewer', uselist=False))
    groups = db.relationship('ProjectReviewerGroup',
                             secondary=reviewer_groups,
                             lazy='subquery',
                             backref=db.backref('reviewers'))

    @property
    def fullname(self):
        return '{} {}'.format(self.firstname, self.lastname)

    def __str__(self):
        return self.fullname


class ProjectReviewRecord(db.Model):
    __tablename__ = 'project_review_records'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    reviewer_id = db.Column('reviewer_id', db.ForeignKey('project_reviewers.id'))
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    comment = db.Column('comment', db.Text(), info={'label': 'สรุปความคิดเห็นและข้อเสนอแนะอื่นๆ'})
    title_comment = db.Column('title_comment', db.Text(), info={'label': 'ความเห็นเกี่ยวกับชื่อโครงการ'})
    status = db.Column('status', db.String(), default='pending',
                       info={
                           'label': 'Decision',
                           'choices': [(i, i) for i in
                                         ('pending', 'revise',
                                          'approved', 'rejected')]
                             },
                       )
    alignment = db.Column('alignment', db.Text())
    alignment_other = db.Column('alignment_other', db.Unicode(),
                                info={'label': 'อื่นๆ'})
    alignment_comment = db.Column('alignment_comment', db.Text(),
                                  info={'label': 'ข้อคิดเห็น'})

    importance = db.Column('importance', db.Unicode(),
                           info={'label': 'ความสำคัญและที่มาของการวิจัย',
                                 'choices': [(c, c) for c in ('ดีมาก', 'ดี', 'พอใช้')]})
    importance_comment = db.Column('importance_comment', db.Text(),
                                   info={'label': 'ข้อคิดเห็น'})

    objective = db.Column('objective', db.Unicode(),
                     info={'label': 'วัตถุประสงค์ของการวิจัย',
                           'choices': [(c, c) for c in ('ชัดเจน', 'ไม่ชัดเจน')]})
    objective_comment = db.Column('objective_comment', db.Text(),
                             info={'label': 'ข้อคิดเห็น'})

    idea = db.Column('idea', db.Unicode(),
                           info={'label': 'แนวคิดพื้นฐาน/กรอบทฤษฎีที่ใช้วิจัย',
                                 'choices': [(c, c) for c in ('ชัดเจน', 'ไม่ชัดเจน')]})
    idea_comment = db.Column('idea_comment', db.Text(),
                                   info={'label': 'ข้อคิดเห็น'})

    sampling = db.Column('sampling', db.Unicode(),
                     info={'label': 'การเลือกกลุ่มตัวอย่าง',
                           'choices': [(c, c) for c in ('ถูกต้อง', 'ควรปรับปรุง')]})
    sampling_comment = db.Column('sampling_comment', db.Text(),
                             info={'label': 'ข้อคิดเห็น'})

    variable = db.Column('variable', db.Unicode(),
                         info={'label': 'การกำหนดตัวแปรต่างๆ',
                               'choices': [(c, c) for c in ('ถูกต้อง', 'ควรปรับปรุง')]})
    variable_comment = db.Column('variable_comment', db.Text(),
                                 info={'label': 'ข้อคิดเห็น'})

    tool = db.Column('tool', db.Unicode(),
                         info={'label': 'เครื่องมือการวิจัยและการตรวจสอบคุณภาพ',
                               'choices': [(c, c) for c in ('ถูกต้อง', 'ควรปรับปรุง')]})
    tool_comment = db.Column('tool_comment', db.Text(),
                                 info={'label': 'ข้อคิดเห็น'})

    data_collection = db.Column('data_collection', db.Unicode(),
                     info={'label': 'การเก็บรวบรวมข้อมูล',
                           'choices': [(c, c) for c in ('ถูกต้อง', 'ควรปรับปรุง')]})
    data_collection_comment = db.Column('data_collection_comment', db.Text(),
                             info={'label': 'ข้อคิดเห็น'})

    data_analyze = db.Column('data_analyze', db.Unicode(),
                                info={'label': 'การวิเคราะห์ข้อมูล',
                                      'choices': [(c, c) for c in ('ถูกต้อง', 'ควรปรับปรุง')]})
    data_analyze_comment = db.Column('data_analyze_comment', db.Text(),
                                        info={'label': 'ข้อคิดเห็น'})

    plan = db.Column('plan', db.Unicode(),
                             info={'label': 'แผนการดำเนินการวิจัย',
                                   'choices': [(c, c) for c in ('เหมาะสม', 'ควรปรับปรุง')]})
    plan_comment = db.Column('plan_comment', db.Text(),
                                     info={'label': 'ข้อคิดเห็น'})

    outcome = db.Column('outcome', db.Unicode(),
                     info={'label': 'ผลผลิตที่ได้จากการวิจัย',
                           'choices': [(c, c) for c in ('เหมาะสม', 'ควรปรับปรุง')]})
    outcome_comment = db.Column('outcome_comment', db.Text(),
                             info={'label': 'ข้อคิดเห็น'})

    outcome_detail = db.Column('outcome_detail', db.Text(),
                        info={'label': 'รายการผลผลิตที่ได้จากการวิจัย'})
    outcome_detail_other = db.Column('outcome_detail_other', db.Unicode(),
                                info={'label': 'อื่นๆ'})

    benefit = db.Column('benefit', db.Unicode(),
                        info={'label': 'ผลประโยชน์ที่คาดว่าจะได้รับ',
                              'choices': [(c, c) for c in ('เหมาะสม', 'ควรปรับปรุง')]})
    benefit_comment = db.Column('benefit_comment', db.Text(),
                                info={'label': 'ข้อคิดเห็น'})

    benefit_detail = db.Column('benefit_detail', db.Text(),
                               info={'label': 'รายการผลประโยชน์ที่คาดว่าจะได้รับ'})
    benefit_detail_other = db.Column('benefit_detail_other', db.Unicode(),
                                     info={'label': 'อื่นๆ'})

    budget = db.Column('budget', db.Unicode(),
                     info={'label': 'งบประมาณ',
                           'choices': [(c, c) for c in ('เหมาะสม', 'ควรปรับปรุง')]})

    budget_comment = db.Column('budget_comment', db.Text(),
                             info={'label': 'ข้อคิดเห็น'})

    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    reviewer = db.relationship('ProjectReviewer',
                               backref=db.backref('records',
                                                  cascade='all, delete-orphan'))
    project = db.relationship('ProjectRecord',
                              backref=db.backref('reviews',
                                                 cascade='all, delete-orphan'))
    file_url = db.Column('file_url', db.Text(), nullable=True, info={'label': 'URL'})
    summarized = db.Column('summarized', db.Boolean(), default=False)
    released_at = db.Column('released_at', db.DateTime(timezone=True))


class ProjectReviewSendRecord(db.Model):
    __tablename__ = 'project_review_send_records'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    review_id = db.Column('review_id', db.ForeignKey('project_review_records.id'))
    sent_at = db.Column('sent_at', db.DateTime(timezone=True))
    title = db.Column('title', db.String(), nullable=False, info={'label': 'Title'})
    message = db.Column('message', db.Text(), info={'label': 'Message'})
    footer = db.Column('footer', db.String(), info={'label': 'Footer'})
    deadline = db.Column('deadline', db.Date())
    review = db.relationship('ProjectReviewRecord',
                             backref=db.backref('send_records',
                                                cascade='all, delete-orphan'))
    to = db.Column('to', db.String())


class ProjectEthicReviewRecord(db.Model):
    __tablename__ = 'project_ethic_review_records'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    reviewer_id = db.Column('reviewer_id', db.ForeignKey('project_reviewers.id'))
    ethic_id = db.Column('ethic_id', db.ForeignKey('project_ethics.id'))
    status = db.Column('status', db.String(), default='pending',
                       info={
                           'label': 'การพิจารณา',
                           'choices': [(i, i) for i in
                                       ('แบบ A ผ่านการพิจารณา', 'แบบ B ผู้วิจัยแก้ไข 3 ชุด ภายใน 4 สัปดาห์',
                                        'แบบ C นำเข้าพิจารณาในที่ประชุม (Full board)', 'แบบ D ไม่อนุมัติ')]
                       })
    project_revision = db.Column('project_revision', db.Text(),
                                 info={'label': 'โครงการวิจัย ขอให้มีการทบทวนดังนี้'})
    tool_revision = db.Column('tool_revision', db.Text(),
                              info={'label': 'เครื่องมือวิจัย เป็นต้นว่าแบบสอบถาม ขอให้มีการทบทวนดังนี้'})
    doc_revision = db.Column('doc_revision', db.Text(),
                             info={'label': 'เอกสารข้อมูลสำหรับกลุ่มประชากรหรือผู้ที่มีส่วนร่วมในการวิจัย (Patient/Participant Information Sheet) ขอให้มีการทบทวนดังนี้'})
    consent_revision = db.Column('consent_revision', db.Text(),
                                 info={'label': 'ใบยินยอมของกลุ่มประชากรหรือผู้มีส่วนร่วมในการวิจัย (Informed consent form) ขอให้มีการทบทวนดังนี้'})
    note = db.Column('note', db.Text(), info={'label': 'ข้อสังเกต'})
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    reviewer = db.relationship('ProjectReviewer', backref=db.backref('ethic_records'))
    ethic = db.relationship('ProjectEthicRecord', backref=db.backref('reviews'))


class ProjectEthicReviewSendRecord(db.Model):
    __tablename__ = 'project_ethic_review_send_records'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    review_id = db.Column('review_id', db.ForeignKey('project_ethic_review_records.id'))
    sent_at = db.Column('sent_at', db.DateTime(timezone=True))
    title = db.Column('title', db.String(), nullable=False, info={'label': 'Title'})
    message = db.Column('message', db.Text(), info={'label': 'Message'})
    footer = db.Column('footer', db.String(), info={'label': 'Footer'})
    deadline = db.Column('deadline', db.Date())
    review = db.relationship('ProjectEthicReviewRecord', backref=db.backref('send_records'))
    to = db.Column('to', db.String())


class ProjectPublicationJournal(db.Model):
    __tablename__ = 'project_pub_journals'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(), nullable=False, info={'label': 'ชื่อวารสาร'})
    abbr = db.Column('abbr', db.String(), info={'label': 'ตัวย่อ'})
    url = db.Column('url', db.String(), info={'label': 'Journal Website URL'})

    def __str__(self):
        return self.name


class ProjectPublication(db.Model):
    __tablename__ = 'project_pub_records'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    journal_id = db.Column('journal_id', db.ForeignKey('project_pub_journals.id'))
    journal = db.relationship(ProjectPublicationJournal, backref=db.backref('articles'))
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    project = db.relationship('ProjectRecord', backref=db.backref('publications'))
    title = db.Column('title', db.String(), nullable=False, info={'label':
                                                                  'Title'})
    volume = db.Column('volume', db.String(), info={'label': 'Volume'})
    doi = db.Column('DOI', db.String(), info={'label': 'DOI'})
    url = db.Column('url', db.String(), info={'label': 'URL'})
    th_abstract = db.Column('th_abstract', db.Text(), info={'label': 'Thai Abstract'})
    en_abstract = db.Column('en_abstract', db.Text(), info={'label': 'English Abstract'})
    issue_no = db.Column('issue_no', db.String(), info={'label': 'Issue No.'})
    indexed = db.Column('indexed', db.String(), info={'label': 'Indexed Database'})
    ranking = db.Column('ranking', db.String(),
                        info={'label': 'Current Journal Ranking',
                              'choices': [(r, r) for r in ['N/A', 'Q1', 'Q2', 'Q3', 'Q4',
                                                           'Tier 1', 'Tier 2']]})
    year = db.Column('year', db.Integer(), info={'label': 'Year'})
    month = db.Column('month', db.String(),
                      info={'choices': [(m, m) for m in ['January', 'February',
                                                       'March', 'April', 'May',
                                                       'June', 'July',
                                                        'August','September',
                                                        'October', 'November',
                                                       'December']],
                            'label': 'Month',
                           })
    page_no = db.Column('page_no', db.String(), info={'label': 'Page No.'})
    category = db.Column('category', db.String(), info={'label': 'Type',
                                                        'choices': [(i, i) for i in
                                                                    ('บทความวิจัย',
                                                                     'บทความวิชาการหรือบทความปริทัศน์'
                                                                     )]})
    creator_id = db.Column(db.ForeignKey('users.id'))
    creator = db.relationship(User)

    @property
    def authors_list(self):
        authors = []
        for a in self.authors:
            if a.user:
                authors.append(str(a.user.profile))
            else:
                authors.append(a.fullname)
        return ', '.join(authors)

    @property
    def pub_date(self):
        if self.year:
            return datetime.strptime('{}-{}-1'.format(self.year, self.month), '%Y-%B-%d')
        else:
            return datetime(2000,1,1)


class ProjectPublicationAuthor(db.Model):
    __tablename__ = 'project_publication_authors'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    pub_id = db.Column('pub_id', db.ForeignKey('project_pub_records.id'))
    pub = db.relationship('ProjectPublication', backref=db.backref('authors', cascade='delete'))
    user_id = db.Column('user_id', db.ForeignKey('users.id'))
    user = db.relationship(User, backref=db.backref('authoreds', cascade='delete'))
    firstname = db.Column('firstname', db.String())
    lastname = db.Column('lastname', db.String())
    affil = db.Column('affiliation', db.String())
    corresponding = db.Column('corresponding', db.Boolean(), default=False)

    #TODO: should add a constructor here for two different use cases.


    @property
    def fullname(self):
        return '{} {}'.format(self.firstname, self.lastname)


class ProjectLanguageEditingSupport(db.Model):
    __tablename__ = 'project_language_editing_supports'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    pub_id = db.Column('pub_id', db.ForeignKey('project_pub_records.id'))
    pub = db.relationship('ProjectPublication', backref=db.backref('language_editing_supports'))
    amount = db.Column('amount', db.Numeric(), default=0.0, info={'label': 'รวมจำนวนที่ขอรับการสนับสนุนการตรวจคุณภาพ/การตรวจทานภาษาของต้นฉบับทั้งสิ้นคือ'})
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    edited_at = db.Column('edited_at', db.DateTime(timezone=True))
    approved_at = db.Column('approved_at', db.DateTime(timezone=True))
    qualification = db.Column('qualification', db.String(),
                              info={'label': 'คุณสมบัติของผู้ขอรับการสนับสนุนตามประกาศฯ'})
    criteria = db.Column('criteria', db.Unicode())
    docs = db.Column('docs', db.Unicode())
    other_docs = db.Column('other_docs', db.Unicode(), info={'label': 'หลักฐานอื่นๆ'})
    request = db.Column('request', db.Unicode())
    status = db.Column('status', db.Unicode(), default='กำลังดำเนินการ',
                       info={'label': 'สถานะ',
                             'choices': [(c, c) for c in ('อนุมัติ', 'ไม่อนุมัติ', 'กำลังดำเนินการ', 'ยกเลิก')]})


class ProjectPublishedReward(db.Model):
    __tablename__ = 'project_pub_rewards'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    pub_id = db.Column('pub_id', db.ForeignKey('project_pub_records.id'))
    pub = db.relationship('ProjectPublication', backref=db.backref('pub_rewards'))
    amount = db.Column('amount', db.Numeric(), default=0.0, info={'label': 'รวมเงินรางวัลทั้งหมด'})
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    edited_at = db.Column('edited_at', db.DateTime(timezone=True))
    approved_at = db.Column('approved_at', db.DateTime(timezone=True))
    qualification = db.Column('qualification', db.String(),
                              info={'label': 'คุณสมบัติของผู้ขอรับการสนับสนุนและรางวัลการตีพิมพ์ผลงานวิชาการ'})
    apc = db.Column('apc', db.Unicode(),
                    info={
                        'label': 'เงินสนับสนุนการตีพิมพ์ผลงานวิชาการ',
                        'choices': [(c, c) for c in (
                                        '',
                                        'วารสารวิชาการระดับชาติ (TCI) IF>0 สนับสนุน 3500 บาท',
                                        'วารสารวิชาการระดับนานาชาติ (ISI/Scopus) Q3 หรือ Q4 สนับสนุน 10000 บาท',
                                        'วารสารวิชาการระดับนานาชาติ (ISI/Scopus) Q1 หรือ Q2 สนับสนุน 20000 บาท',
                                    )]
                    })
    reward = db.Column('reward', db.Unicode(),
                       info={
                           'label': 'เงินรางวัลการตีพิมพ์ผลงานวิชาการ',
                           'choices': [(c, c) for c in (
                                        '',
                                        'บทความวิจัยระดับชาติ IF 0.0-1.0 รางวัล 2000 บาท',
                                        'บทความวิจัยระดับชาติ IF 1.0-2.0 รางวัล 4000 บาท',
                                        'บทความวิจัยระดับชาติ IF > 2.0 รางวัล 6000 บาท',
                                        'บทความวิชาการหรือปรทัศน์ระดับชาติ IF 0.0-1.0 รางวัล 1000 บาท',
                                        'บทความวิชาการหรือปรทัศน์ระดับชาติ IF 1.0-2.0 รางวัล 2000 บาท',
                                        'บทความวิชาการหรือปรทัศน์ระดับชาติ IF > 2.0 รางวัล 3000 บาท',
                                        'บทความวิจัยระดับนานาชาติ Q4 รางวัล 5000 บาท',
                                        'บทความวิจัยระดับนานาชาติ Q3 รางวัล 10000 บาท',
                                        'บทความวิจัยระดับนานาชาติ Q2 รางวัล 15000 บาท',
                                        'บทความวิจัยระดับนานาชาติ Q1 รางวัล 20000 บาท',
                                        'บทความวิชาการหรือปริทัศน์ระดับนานาชาติ Q4 รางวัล 3000 บาท',
                                        'บทความวิชาการหรือปริทัศน์ระดับนานาชาติ Q3 รางวัล 6000 บาท',
                                        'บทความวิชาการหรือปริทัศน์ระดับนานาชาติ Q2 รางวัล 9000 บาท',
                                        'บทความวิชาการหรือปริทัศน์ระดับนานาชาติ Q1 รางวัล 12000 บาท',
                                    )]
                       })
    status = db.Column('status', db.Unicode(), default='กำลังดำเนินการ',
                       info={'label': 'สถานะ',
                             'choices': [(c, c) for c in ('อนุมัติ', 'ไม่อนุมัติ', 'กำลังดำเนินการ', 'ยกเลิก')]})


class ProjectProposalDevelopmentSupport(db.Model):
    __tablename__ = 'project_proposal_development_supports'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    qualification = db.Column('qualification', db.String())
    support = db.Column('support', db.String(),
                        info={'label': 'ขอรับเงินสนับสนุนโครงการให้คำปรึกษาเพื่อพัฒนาข้อเสนอโครงการวิจัยหรือแผนงานวิจัยและสถิติการวิจัย',
                              'choices': [(c,c) for c in (
                                  'แหล่งทุนภายนอกไม่เกิน 30,000 บาท ขอรับเงินสนับสนุนได้ไม่เกิน 1,000 บาท',
                                  'แหล่งทุนภายนอกไม่เกิน 30,000-100,000 บาท ขอรับเงินสนับสนุนได้ไม่เกิน 2,000 บาท',
                                  'แหล่งทุนภายนอกไม่เกิน 100,000-300,000 บาท ขอรับเงินสนับสนุนได้ไม่เกิน 3,000 บาท',
                                  'แหล่งทุนภายนอกไม่เกิน 300,000-500,000 บาท ขอรับเงินสนับสนุนได้ไม่เกิน 4,000 บาท',
                                  'แหล่งทุนภายนอกมากกว่า 500,000 บาทขึ้นไป ขอรับเงินสนับสนุนได้ไม่เกิน 5,000 บาท',
                                  'แหล่งทุนภายในไม่เกิน 30,000 บาท ขอรับเงินสนับสนุนได้ไม่เกิน 1,000 บาท',
                                  'แหล่งทุนภายในไม่เกิน 30,000-100,000 บาท ขอรับเงินสนับสนุนได้ไม่เกิน 2,000 บาท',
                                  'แหล่งทุนภายในมากกว่า 100,000 บาทขึ้นไป ขอรับเงินสนับสนุนได้ไม่เกิน 3,000 บาท',
                              )]})
    docs = db.Column('docs', db.Text())
    other_docs = db.Column('other_docs', db.String(),
                           info={'label': 'เอกสารอื่นๆ (ถ้ามี)'})
    project = db.relationship('ProjectRecord', backref=db.backref('proposal_development_supports'))
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    edited_at = db.Column('edited_at', db.DateTime(timezone=True))
    approved_at = db.Column('approved_at', db.DateTime(timezone=True))
    contract_file_url = db.Column('contract_file_url', db.String())


class ProjectSupplementaryDocument(db.Model):
    __tablename__ = 'project_supplementary_docs'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    filename = db.Column('filename', db.String(), info={'label': 'ชื่อไฟล์'})
    desc = db.Column('desc', db.Text(), info={'label': 'รายละเอียด'})
    file_url = db.Column('file_url', db.String(), info={'label': 'URL'})
    project = db.relationship('ProjectRecord', backref=db.backref('supplementary_docs'))


class ProjectCVFile(db.Model):
    __tablename__ = 'project_cv_files'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    project_id = db.Column('project_id', db.ForeignKey('projects.id'))
    filename = db.Column('filename', db.String(), info={'label': 'ชื่อไฟล์'})
    file_url = db.Column('file_url', db.String(), info={'label': 'URL'})
    project = db.relationship('ProjectRecord', backref=db.backref('cv_files'))


sqlalchemy.orm.configure_mappers()
