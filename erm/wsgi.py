from app import create_app
from pytz import timezone
from flask import render_template
from app import admin, db
from app.main.models import User, MailInfo
from app.researcher.models import Profile, Program, Department, Education
from app.project.models import *
from flask_admin.contrib.sqla import ModelView
from werkzeug.exceptions import InternalServerError, BadRequest, NotFound


app = create_app()


@app.errorhandler(NotFound)
def handle_not_found_error(e):
    error_message = u'ขออภัย ไม่พบหน้าเพจที่ท่านเรียก'
    return render_template('main/error_page.html',
                           error_obj=e, error_message=error_message)


@app.errorhandler(InternalServerError)
def handle_internal_server_error(e):
    error_message = u'ขออภัยระบบขัดข้องบางประการโปรดติดต่อศูนย์วิจัยเพื่อตรวจสอบและแก้ไข'
    return render_template('main/error_page.html',
                           error_obj=e, error_message=error_message)


@app.errorhandler(BadRequest)
def handle_bad_request_error(e):
    error_message = u'ขออภัยระบบขัดข้องเนื่องจากข้อมูลผิดพลาดโปรดตรวจสอบข้อมูลอีกครั้ง'
    return render_template('main/error_page.html',
                           error_obj=e, error_message=error_message)


@app.template_filter("localdatetime")
def local_datetime(dt):
    if dt is None:
        return ''
    bangkok = timezone('Asia/Bangkok')
    datetime_format = '%d/%m/%Y %H:%M'
    return dt.astimezone(bangkok).strftime(datetime_format)


@app.template_filter("localdate")
def local_datetime(dt):
    bangkok = timezone('Asia/Bangkok')
    datetime_format = '%d/%m/%Y'
    return dt.strftime(datetime_format)


@app.context_processor
def utility_processor():
    # the context processor returns a dictionary that will be injected into the template context
    def sum_objects(obj_list, attr):
        return sum([getattr(obj, attr) for obj in obj_list])
    return {'sum_objs': sum_objects}


@app.template_filter("format_number")
def format_number(number, formatting='{0:.2f}', currency=''):
    return formatting.format(number) + ' ' + currency


admin.add_view(ModelView(User, db.session, category='Main'))
admin.add_view(ModelView(MailInfo, db.session, category='Main'))
admin.add_view(ModelView(Profile, db.session, category='Researcher'))
admin.add_view(ModelView(Program, db.session, category='Researcher'))
admin.add_view(ModelView(Department, db.session, category='Researcher'))



class EducationModelView(ModelView):
    form_choices = {
        'degree': [('Bachelor', 'Bachelor'), ('Master', 'Master'), ('Doctorate', 'Doctorate')]
    }

admin.add_view(EducationModelView(Education, db.session, category='Researcher'))

class ProjectMemberModelView(ModelView):
    form_choices = {
        'role': [('PI', 'PI'),
                 ('co-PI', 'co-PI'),
                 ('Researcher', 'Researcher'),
                 ('Coordinator', 'Coordinator'),
                 ]
    }


class ProjectRecordModelView(ModelView):
    can_view_details = True
    form_widget_args = {
        'intro': {
            'rows': 10,
        },
        'abstract': {
            'rows': 10
        },
        'method': {
            'rows': 10
        },
        'objective': {
            'rows': 10
        },
    }
    form_choices = {
        'status': [('draft', 'draft'), ('submitted', 'submitted'),
                   ('concept', 'concept'), ('full', 'full',),
                   ('revising', 'revising'),
                   ('rejected', 'rejected'),
                   ('finished', 'finished')]
    }


class ProjectFundSourceModelView(ModelView):
    form_choices = {
        'from_': [(c, c) for c in ('ภายนอก', 'ภายใน')]
    }


admin.add_view(ProjectRecordModelView(ProjectRecord, db.session, category='Project'))
admin.add_view(ProjectMemberModelView(ProjectMember, db.session, category='Project'))
admin.add_view(ModelView(Category, db.session, category='Project'))
admin.add_view(ModelView(SubCategory, db.session, category='Project'))
admin.add_view(ModelView(Application, db.session, category='Project'))
admin.add_view(ModelView(ProjectReviewerGroup, db.session, category='Project'))
admin.add_view(ModelView(ProjectReviewer, db.session, category='Project'))
admin.add_view(ModelView(ProjectReviewRecord, db.session, category='Project'))
admin.add_view(ModelView(ProjectEthicRecord, db.session, category='Project'))
admin.add_view(ModelView(ProjectEthicReviewRecord, db.session, category='Project'))
admin.add_view(ModelView(ProjectEthicReviewSendRecord, db.session, category='Project'))
admin.add_view(ModelView(ProjectPublicationJournal, db.session, category='Project'))
admin.add_view(ModelView(ProjectPublication, db.session, category='Project'))
admin.add_view(ModelView(ProjectPublicationAuthor, db.session, category='Project'))
admin.add_view(ModelView(ProjectLanguageEditingSupport, db.session, category='Project'))
admin.add_view(ModelView(ProjectMilestone, db.session, category='Project'))
admin.add_view(ModelView(ProjectBudgetCategory, db.session, category='Project'))
admin.add_view(ModelView(ProjectBudgetSubCategory, db.session, category='Project'))
admin.add_view(ModelView(ProjectBudgetItem, db.session, category='Project'))
admin.add_view(ModelView(ProjectBudgetItemOverall, db.session, category='Project'))
admin.add_view(ModelView(ParentProjectRecord, db.session, category='Project'))
admin.add_view(ProjectFundSourceModelView(ProjectFundSource, db.session, category='Project'))
