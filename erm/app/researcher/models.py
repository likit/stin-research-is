from app import db
from app.main.models import User
from wtforms.fields import FileField


class Department(db.Model):
    __tablename__ = 'departments'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name_th = db.Column('name_th', db.String(),
                        nullable=False, unique=True,
                        info={'label': 'TH Name'})
    name_en = db.Column('name_en', db.String(), unique=True,
                        info={'label': 'EN Name'})

    def __str__(self):
        return self.name_th


class Program(db.Model):
    __tablename__ = 'programs'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name_th = db.Column('name_th', db.String(), nullable=False, unique=True)
    name_en = db.Column('name_en', db.String(), unique=True)
    dept_id = db.Column('dept_id', db.ForeignKey('departments.id'))
    dept = db.relationship(Department, backref=db.backref('programs'))

    def __str__(self):
        return self.name_th


class Education(db.Model):
    __tablename__ = 'educations'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    degree = db.Column('degree',
                       db.String(),
                       info={'choices': [(i, i) for i in ['Bachelor', 'Master', 'Doctorate']]},
                       nullable=False)
    degree_title = db.Column('degree_title', db.String())
    field = db.Column('field', db.String())
    program = db.Column('program', db.String())
    university = db.Column('university', db.String())
    year = db.Column('year', db.Integer, nullable=False)
    profile_id = db.Column('profile_id', db.ForeignKey('profiles.id'))
    profile = db.relationship('Profile', backref=db.backref('educations'))


class Profile(db.Model):
    __tablename__ = 'profiles'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column('user_id', db.ForeignKey('users.id'))
    user = db.relationship(User, backref=db.backref('profile', uselist=False))
    photo_url = db.Column('photo_url', db.String(), nullable=True)
    title_th = db.Column('title_th', db.String(), info={'label': 'คำนำหน้า'})
    title_en = db.Column('title_en', db.String(), info={'label': 'Title'})
    firstname_th = db.Column('firstname_th', db.String(), info={'label': 'ชื่อ'})
    lastname_th = db.Column('lastname_th', db.String(), info={'label': 'นามสกุล'})
    firstname_en = db.Column('firstname_en', db.String(), info={'label': 'First Name'})
    lastname_en = db.Column('lastname_en', db.String(), info={'label': 'Last Name'})
    program_id = db.Column('program_id', db.ForeignKey('programs.id'))
    program = db.relationship(Program, backref=db.backref('researchers'))
    position = db.Column('position', db.String(), info={'label': 'ตำแหน่งปัจจุบัน'})
    field_expertise = db.Column('field_expertise', db.String(), info={'label': 'สาขาวิชาการที่มีความชำนาญพิเศษ'})
    experience = db.Column('experience', db.Text(), info={'label': 'ประสบการณ์ที่เกี่ยวข้องกับการบริหารงานวิจัย'})

    def __init__(self, user_id=None):
        self.user_id = user_id

    def __str__(self):
        return self.fullname_th

    @property
    def fullname_th(self):
        return '{} {}'.format(self.firstname_th, self.lastname_th)

    @property
    def fullname_en(self):
        return '{} {}'.format(self.firstname_en, self.lastname_en)

    @property
    def affiliation(self):
        return '{} {}'.format(self.program, self.program.department)


class IntlConferenceSupport(db.Model):
    __tablename__ = 'researcher_intl_conference_supports'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    qualification = db.Column('qualification', db.String())
    article_title = db.Column('article_title', db.String(), info={'label': 'ชื่อผลงานวิจัย'})
    organizer = db.Column('organizer', db.String(), info={'label': 'หน่วยงานผู้จัดประชุม'})
    venue = db.Column('venue', db.String(), info={'label': 'สถานที่จัดประชุม'})
    conference_date = db.Column('conference_date', db.Date(), info={'label': 'วันที่จัดประชุม'})
    presentation_date = db.Column('presentation_date', db.Date(), info={'label': 'วันที่นำเสนอผลงาน'})
    presentation_type = db.Column('presentation_type', db.String(), info={'label': 'ประเภทการนำเสนอ'})
    amount = db.Column('amount', db.Numeric(), default=0.0, info={'label': 'จำนวนเงินที่ขอสนับสนุน'})
    researcher_id = db.Column('researcher_id', db.ForeignKey('users.id'))
    researcher = db.relationship(User, backref=db.backref('intl_conference_supports'))
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    edited_at = db.Column('edited_at', db.DateTime(timezone=True))
    approved_at = db.Column('approved_at', db.DateTime(timezone=True))


class DevelopmentType(db.Model):
    __tablename__ = 'researcher_development_types'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(), nullable=False, info={'label': 'ประเภท'})


class DevelopmentCategory(db.Model):
    __tablename__ = 'researcher_development_categories'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    name = db.Column('name', db.String(), nullable=False, info={'label': 'หมวด'})


class DevelopmentRecord(db.Model):
    __tablename__ = 'researcher_development_records'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    topic = db.Column('topic', db.String(), nullable=False, info={'label': 'หัวข้อ'})
    researcher_id = db.Column('researcher_id', db.ForeignKey('users.id'))
    researcher = db.relationship(User, backref=db.backref('development_records'))
    venue = db.Column('venue', db.String(), info={'label': 'สถานที่จัดประชุม'})
    start_date = db.Column('start_date', db.Date(), info={'label': 'วันที่เริ่มต้น'})
    end_date = db.Column('end_date', db.Date(), info={'label': 'วันที่สิ้นสุด'})
    submitted_at = db.Column('submitted_at', db.DateTime(timezone=True))
    edited_at = db.Column('edited_at', db.DateTime(timezone=True))
    approved_at = db.Column('approved_at', db.DateTime(timezone=True))
    rejected_at = db.Column('rejected_at', db.DateTime(timezone=True))
    development_type_id = db.Column(db.ForeignKey('researcher_development_types.id'))
    development_type = db.relationship(DevelopmentType, backref=db.backref('records'))
    development_category_id = db.Column(db.ForeignKey('researcher_development_categories.id'))
    development_category = db.relationship(DevelopmentCategory, backref=db.backref('records'))
    file_url = db.Column('file_url', db.String())


class DevelopmentExpenseItem(db.Model):
    __tablename__ = 'researcher_development_expense_items'
    id = db.Column('id', db.Integer, primary_key=True, autoincrement=True)
    item = db.Column('item', db.String(), nullable=True, info={'label': 'รายการ'})
    amount = db.Column('amount', db.Float(), info={'label': 'จำนวนเงิน'})
    record_id = db.Column(db.ForeignKey('researcher_development_records.id'))
    record = db.relationship(DevelopmentRecord, backref=db.backref('items'))
