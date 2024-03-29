import os
import uuid

import arrow
import pypandoc
import requests
from collections import defaultdict

from app.webadmin import webadmin_bp as webadmin
from flask_login import login_required
from app import superuser
from flask import render_template, redirect, url_for, request, flash, send_file
from werkzeug.utils import secure_filename
from app import mail
from app.researcher.forms import IntlConferenceSupportForm, DevelopmentTypeForm, DevelopmentCategoryForm
from app.researcher.models import IntlConferenceSupport, DevelopmentType, DevelopmentCategory, DevelopmentRecord
from app.project.models import *
from app.webadmin.forms import (ProjectReviewSendRecordForm, ProjectReviewRecordForm,
                                ProjectEthicReviewSendRecordForm,
                                ProjectEthicReviewRecordForm, ProjectEthicRecordForm, ProjectReviewRecordAdminForm,
                                )
from app.project.forms import *
from app.main.models import User, MailInfo
from pydrive.auth import ServiceAccountCredentials, GoogleAuth
from pydrive.drive import GoogleDrive
from flask_mail import Message
from itsdangerous import TimedJSONWebSignatureSerializer

import pandas as pd

from app.project.models import ProjectRecord, ProjectReviewRecord

gauth = GoogleAuth()
keyfile_dict = requests.get(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS')).json()
scopes = ['https://www.googleapis.com/auth/drive']
gauth.credentials = ServiceAccountCredentials.from_json_keyfile_dict(keyfile_dict, scopes)
drive = GoogleDrive(gauth)

GANTT_ACTIVITIES = dict([(1, '1. พัฒนาโครงร่างการวิจัยและเครื่องมือการวิจัย'),
                         (2, '2. เสนอโครงร่างการวิจัยเพื่อขอรับการพิจารณาจริยธรรมฯ'),
                         (3, '3. เสนอขอรับทุนอุดหนุนการวิจัย'),
                         (4, '4. ผู้ทรงคุณวุฒิตรวจสอบและแก้ไข'),
                         (5, '5. ติดต่อประสานงานเพื่อขอเก็บข้อมูล'),
                         (6, '6. ดำเนินการเก็บรวบรวมข้อมูล'),
                         (7, '7. วิเคราะห์ผลการวิจัยและอภิปรายผล'),
                         (8, '8. จัดทำรายงานการวิจัยและเตรียมต้นฉบับตีพิมพ์งานวิจัย')]
                        )

STIN_EMAIL = os.environ.get('MAIL_USERNAME')


def send_mail(recp, title, message):
    mail_info = MailInfo.query.first()
    signature = '\n\n-----------------------\n' + mail_info.signature
    message = Message(subject=title, body=message + signature, recipients=[recp])
    mail.send(message)


@webadmin.route('/submissions')
@superuser
@login_required
def list_submissions():
    submissions = ProjectRecord.query.filter(ProjectRecord.status.endswith('submitted'))
    return render_template('webadmin/submissions.html', submissions=submissions)


@webadmin.route('/submissions/<int:project_id>')
@superuser
@login_required
def submission_detail(project_id):
    project = ProjectRecord.query.get(project_id)
    gantt_activities = []
    for a in sorted(project.gantt_activities, key=lambda x: x.task_id):
        gantt_activities.append([
            str(a.task_id),
            GANTT_ACTIVITIES.get(a.task_id),
            a.start_date.isoformat(),
            a.end_date.isoformat(),
            None, 0, None,
            a.start_date,
            a.end_date,
            a.id
        ])
    return render_template('webadmin/submission_detail.html',
                           project=project,
                           gantt_activities=gantt_activities
                           )


@webadmin.route('/submissions/<int:project_id>/ethics/<int:ethic_id>/reviewers/add')
@superuser
@login_required
def list_reviewers(project_id, ethic_id):
    project = ProjectRecord.query.get(project_id)
    groups = ProjectReviewerGroup.query.all()
    return render_template('webadmin/reviewers_add.html',
                           project=project,
                           groups=groups,
                           ethic_id=ethic_id)


@webadmin.route('/submissions/<int:project_id>/reviewers/add')
@superuser
@login_required
def list_project_reviewers(project_id):
    project = ProjectRecord.query.get(project_id)
    groups = ProjectReviewerGroup.query.all()
    return render_template('webadmin/reviewers_add.html',
                           project=project, groups=groups)


@webadmin.route('/submissions/<int:project_id>/reviewers/add/<int:reviewer_id>')
@superuser
@login_required
def add_reviewer(project_id, reviewer_id):
    review = ProjectReviewRecord.query.filter_by(reviewer_id=reviewer_id,
                                                 project_id=project_id).first()
    if not review:
        review = ProjectReviewRecord(
            project_id=project_id,
            reviewer_id=reviewer_id
        )
        db.session.add(review)
        db.session.commit()
        flash('Reviewer has been added to the project review.', 'success')
    return redirect(request.referrer)


@webadmin.route('/submissions/<int:project_id>/reviewers/add/all/<int:group_id>')
@superuser
@login_required
def add_all_reviewers(project_id, group_id):
    reviewer_group = ProjectReviewerGroup.query.get(group_id)
    project = ProjectRecord.query.get(project_id)
    for reviewer in reviewer_group.reviewers:
        if reviewer not in project.reviewers:
            review = ProjectReviewRecord(reviewer=reviewer, project=project)
            db.session.add(review)
    db.session.commit()
    flash('All reviewers have been added to the project review.', 'success')
    return redirect(request.referrer)


@webadmin.route('/submissions/<int:project_id>/reviewers/remove/<int:reviewer_id>')
@superuser
@login_required
def remove_reviewer(project_id, reviewer_id):
    review = ProjectReviewRecord.query.filter_by(reviewer_id=reviewer_id,
                                                 project_id=project_id).first()
    db.session.delete(review)
    db.session.commit()
    flash('Reviewer has been removed to the project review.', 'success')
    return redirect(request.referrer)


@webadmin.route('/submissions/<int:project_id>/reviewers/remove/all')
@superuser
@login_required
def remove_all_reviewers(project_id):
    project = ProjectRecord.query.get(project_id)
    for review in project.reviews:
        db.session.delete(review)
        db.session.commit()
    flash('All reviewers have been removed to the project review.', 'success')
    return redirect(request.referrer)


@webadmin.route('/submissions/<int:project_id>/reviews', methods=['GET', 'POST'])
@superuser
@login_required
def view_reviews(project_id):
    project = ProjectRecord.query.get(project_id)
    review = ProjectReviewRecord.query.filter_by(project_id=project.id,
                                                 summarized=True).first()
    if review:
        form = ProjectReviewRecordAdminForm(obj=review)
        form.alignment_select.data = review.alignment.split('|')
        form.outcome_detail_select.data = review.outcome_detail.split('|')
        form.benefit_detail_select.data = review.benefit_detail.split('|')
        released = request.args.get('released', 'no')
        if (released == 'yes') and (review.released_at is None):
            review.released_at = arrow.now(tz='Asia/Bangkok').datetime
            db.session.add(review)
            db.session.commit()
            # TODO: send an email to notify the project coordinator
            flash('The review has been released.', 'success')
    else:
        form = ProjectReviewRecordAdminForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            if review is None:
                review = ProjectReviewRecord()
            form.populate_obj(review)
            review.summarized = True
            review.project = project
            review.alignment = '|'.join(form.alignment_select.data)
            review.outcome_detail = '|'.join(form.outcome_detail_select.data)
            review.benefit_detail = '|'.join(form.benefit_detail_select.data)
            review.submitted_at = arrow.now(tz='Asia/Bangkok').datetime
            db.session.add(review)
            db.session.commit()
            flash('Review has been saved.', 'success')
        else:
            # flash('โปรดกรอกข้อมูลที่จำเป็นให้ครบ', 'danger')
            flash(form.errors, 'danger')
    return render_template('webadmin/reviews.html', project=project, form=form, review=review)


@webadmin.route('/submissions/<int:project_id>/reviews/<int:review_id>/summary/export')
@superuser
@login_required
def export_review(project_id, review_id):
    project = ProjectRecord.query.get(project_id)
    review = ProjectReviewRecord.query.get(review_id)
    members = []
    for member in project.members:
        if member.user:
            members.append('{} ({})'.format(member.user.profile.fullname_th, member.role))
        else:
            members.append('{} ({})'.format(member.fullname, member.affil))

    def generate():
        content = '<h1>โครงการวิจัย</h1>'
        content += '<hr>'
        content += '<h2>ชื่อภาษาไทย</h2>'
        content += '<p>{}</p>'.format(project.title_th)
        content += '<h2>ชื่อรองภาษาไทย</h2>'
        content += '<p>{}</p>'.format(project.subtitle_th)
        content += '<h2>ชื่อภาษาอังกฤษ</h2>'
        content += '<p>{}</p>'.format(project.title_en)
        content += '<h2>ชื่อรองภาษาอังกฤษ</h2>'
        content += '<p>{}</p>'.format(project.subtitle_en)
        content += '<h2>แหล่งทุน</h2>'
        content += '<p>{}</p>'.format(project.fund_source.name)
        content += '<h2>ที่ปรึกษาโครงการ</h2>'
        content += '<p>{}</p>'.format(project.mentor)
        content += '<h2>คณะผู้วิจัย</h2>'
        content += '<p>{}</p>'.format(', '.join(members))
        content += '<h2>สรุปผลการประเมิน</h2>'
        content += '<table border="1">'
        content += '<thead>'
        content += '<th>หัวข้อ</th>'
        content += '<th>ผลการประเมิน</th>'
        content += '<th>คำแนะนำ</th>'
        content += '</thead>'
        content += '<tbody>'
        content += '<tr><td><strong>ความสอดคล้องกับยุทธศาสตร์</strong></td>'
        content += '<td>'
        content += '<ul>'
        for aln in review.alignment.split('|'):
            content += '<li>{}</li>'.format(aln)
        content += '</ul>'
        content += '</td></tr>'
        content += '<tr><td><strong>ความเห็นเกี่ยวกับชื่อโครงการวิจัย</strong></td>'
        content += '<td></td>'
        content += '<td>{}</td>'.format(review.title_comment)
        content += '</tr>'
        content += '<tr><td><strong>วัตถุประสงค์</strong></td>'
        content += '<td>{}</td>'.format(review.objective)
        content += '<td>{}</td>'.format(review.objective_comment or '-')
        content += '</tr>'
        content += '<tr><td><strong>ความสำคัญและที่มาของปัญหาการวิจัย</strong></td>'
        content += '<td>{}</td>'.format(review.importance)
        content += '<td>{}</td>'.format(review.importance_comment or '-')
        content += '</tr>'
        content += '<tr><td><strong>แนวคิดพื้นฐาน/กรอบทฤษฎีที่ใช้ในการวิจัย</strong></td>'
        content += '<td>{}</td>'.format(review.idea)
        content += '<td>{}</td>'.format(review.idea_comment or '-')
        content += '</tr>'
        content += '<tr><td><strong>ระเบียบวิธีวิจัย</strong></td>'
        content += '<td colspan=2>'
        content += '<table border="1">'
        content += '<thead><th></th><th>ผลการประเมิน</th><th>คำแนะนำ</th></thead>'
        content += '<tbody>'
        content += '<tr><td><strong>การเลือกกลุ่มตัวอย่าง</strong></td>'
        content += '<td>{}</td>'.format(review.sampling)
        content += '<td>{}</td>'.format(review.sampling_comment or '-')
        content += '</tr>'
        content += '<tr><td><strong>การกำหนดตัวแปรต่าง ๆ</strong></td>'
        content += '<td>{}</td>'.format(review.variable)
        content += '<td>{}</td>'.format(review.variable_comment or '-')
        content += '</tr>'
        content += '<tr><td><strong>เครื่องมือการวิจัยฯ</strong></td>'
        content += '<td>{}</td>'.format(review.tool)
        content += '<td>{}</td>'.format(review.tool_comment or '-')
        content += '</tr>'
        content += '<tr><td><strong>การเก็บรวบรวมข้อมูล</strong></td>'
        content += '<td>{}</td>'.format(review.data_collection)
        content += '<td>{}</td>'.format(review.data_collection_comment or '-')
        content += '</tr>'
        content += '<tr><td><strong>วิธีการวิเคราะห์ข้อมูล</strong></td>'
        content += '<td>{}</td>'.format(review.data_analyze)
        content += '<td>{}</td>'.format(review.data_analyze_comment or '-')
        content += '</tr>'
        content += '</tbody>'
        content += '</table>'
        content += '</td>'
        content += '</tr>'
        content += '<tr><td><strong>แผนการดำเนินการวิจัย</strong></td>'
        content += '<td>{}</td>'.format(review.plan)
        content += '<td>{}</td>'.format(review.plan_comment or '-')
        content += '</tr>'
        content += '<tr><td><strong>ผลผลิตจากการวิจัย</strong></td>'
        content += '<td>{}</td>'.format(review.outcome)
        content += '<td>{}</td>'.format(review.outcome_comment or '-')
        content += '</tr>'
        content += '<tr><td><strong>รายการผลผลิตจากการวิจัย</strong></td>'
        content += '<td>'
        content += '<ul>'
        for aln in review.outcome_detail.split('|'):
            content += '<li>{}</li>'.format(aln)
        content += '</ul>'
        content += '<td>{}</td>'.format(review.outcome_detail_other or '-')
        content += '</tr>'
        content += '<tr><td><strong>ประโยชน์ที่คาดว่าจะได้รับ</strong></td>'
        content += '<td>{}</td>'.format(review.benefit)
        content += '<td>{}</td>'.format(review.benefit_comment or '-')
        content += '</tr>'
        content += '<tr><td><strong>รายการประโยชน์ที่คาดว่าจะได้รับ</strong></td>'
        content += '<td>'
        content += '<ul>'
        for aln in review.benefit_detail.split('|'):
            content += '<li>{}</li>'.format(aln)
        content += '</ul>'
        content += '<td>{}</td>'.format(review.benefit_detail_other or '-')
        content += '</tr>'
        content += '<tr><td><strong>งบประมาณ</strong></td>'
        content += '<td>{}</td>'.format(review.budget)
        content += '<td>{}</td>'.format(review.budget_comment or '-')
        content += '</tr>'
        content += '<tr><td><strong>สรุป</strong></td>'
        content += '<td colspan=2>{}</td>'.format(review.comment)
        content += '</tr>'
        content += '<tr><td><strong>ผลการตัดสิน</strong></td>'
        content += '<td colspan=2>{}</td>'.format(review.status)
        content += '</tr>'
        content += '</tbody>'
        content += '</table>'

        pypandoc.convert_text(content, 'docx',
                              format='html',
                              outputfile='app/summary.docx')

    generate()

    return send_file('summary.docx')


@webadmin.route('/submissions/<int:project_id>/reviews/send', methods=['GET', 'POST'])
@superuser
@login_required
def send_for_reviews(project_id):
    project = ProjectRecord.query.get(project_id)
    form = ProjectReviewSendRecordForm()
    if request.method == 'POST':
        serializer = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'),
                                                     expires_in=1814400)
        if form.validate_on_submit():
            unsubmitted = [r for r in project.reviews if r.submitted_at is None]
            if not unsubmitted:
                new_review = ProjectReviewRecord(project_id=project_id,
                                                 reviewer_id=project.reviews[0].reviewer_id)
                db.session.add(new_review)
                db.session.commit()
                token = serializer.dumps({'review_id': new_review.id})
                url = url_for('webadmin.write_review',
                              project_id=project.id,
                              review_id=new_review.id,
                              token=token,
                              _external=True)
                message = \
                    '{}\n\nกรุณาคลิกที่ลิงค์ด้านล่างเพื่อดำเนินการจักเป็นพระคุณยิ่ง\n\n{}' \
                    '\n\nขอความกรุณาส่งผลการประเมินภายในวันที่ {}\n\n{}' \
                        .format(form.message.data, url, form.deadline.data.strftime('%d/%m/%Y'), form.footer.data)
                try:
                    send_mail(new_review.reviewer.email, title=form.title.data, message=message)
                except:
                    flash('Failed to send an email to {}'.format(new_review.reviewer.email), 'danger')
                else:
                    new_send = ProjectReviewSendRecord()
                    form.populate_obj(new_send)
                    new_send.review_id = new_review.id
                    new_send.to = new_review.reviewer.email
                    new_send.sent_at = arrow.now(tz='Asia/Bangkok').datetime,
                    db.session.add(new_send)

            for review in unsubmitted:
                token = serializer.dumps({'review_id': review.id})
                url = url_for('webadmin.write_review',
                              project_id=project.id,
                              review_id=review.id,
                              token=token,
                              _external=True)

                message = '{}\n\nกรุณาคลิกที่ลิงค์ด้านล่างเพื่อดำเนินการจักเป็นพระคุณยิ่ง\n\n{}\n\nขอความกรุณาส่งผลการประเมินภายในวันที่ {}\n\n{}' \
                    .format(form.message.data, url, form.deadline.data.strftime('%d/%m/%Y'), form.footer.data)
                try:
                    send_mail(review.reviewer.email, title=form.title.data, message=message)
                except:
                    flash('Failed to send an email to {}'.format(review.reviewer.email), 'danger')
                else:
                    new_send = ProjectReviewSendRecord()
                    form.populate_obj(new_send)
                    new_send.review_id = review.id
                    new_send.to = review.reviewer.email
                    new_send.sent_at = arrow.now(tz='Asia/Bangkok').datetime,
                    db.session.add(new_send)
                # only allow sending one unsubmitted review
                break
            db.session.commit()
            print(unsubmitted)
            flash('The project has been sent for all reviewers.', 'success')
            return redirect(url_for('webadmin.submission_detail',
                                    project_id=project.id))
        else:
            flash(form.errors, 'danger')

    return render_template('webadmin/send_reviews.html', form=form, project=project)


@webadmin.route('/submissions/<int:project_id>/reviews/send/<int:reviewer_id>',
                methods=['GET', 'POST'])
@superuser
@login_required
def send_for_review_single(project_id, reviewer_id=None):
    project = ProjectRecord.query.get(project_id)
    reviewer = ProjectReviewer.query.get(reviewer_id)
    form = ProjectReviewSendRecordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            review = ProjectReviewRecord.query.filter_by(reviewer_id=reviewer_id,
                                                         project_id=project_id).first()
            if review:
                serializer = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'),
                                                             expires_in=1814400)
                token = serializer.dumps({'review_id': review.id})
                url = url_for('webadmin.write_review',
                              project_id=project.id,
                              review_id=review.id,
                              token=token,
                              _external=True)

                message = '{}\n\nกรุณาคลิกที่ลิงค์ด้านล่างเพื่อดำเนินการจักเป็นพระคุณยิ่ง\n\n{}\n\nขอความกรุณาส่งผลการประเมินภายในวันที่ {}\n\n{}' \
                    .format(form.message.data, url, form.deadline.data.strftime('%d/%m/%Y'), form.footer.data)
                try:
                    send_mail(review.reviewer.email,
                              title=form.title.data,
                              message=message)
                except:
                    flash('Failed to send an email to {}'.format(review.reviewer.email), 'danger')
                else:
                    new_send = ProjectReviewSendRecord()
                    form.populate_obj(new_send)
                    new_send.review_id = review.id
                    new_send.to = review.reviewer.email
                    new_send.sent_at = arrow.now(tz='Asia/Bangkok').datetime,
                    db.session.add(new_send)
                db.session.commit()
                flash('The project has been sent for all reviewers.', 'success')
                return redirect(url_for('webadmin.submission_detail',
                                        project_id=project.id))
            else:
                flash('Reviewer does not exists.', 'danger')
        else:
            flash(form.error, 'danger')
    return render_template('webadmin/send_reviews.html',
                           form=form, project=project, to=reviewer)


@webadmin.route('/submissions/<int:project_id>/reviews/sends', methods=['GET', 'POST'])
@superuser
@login_required
def view_send_records(project_id):
    project = ProjectRecord.query.get(project_id)
    return render_template('webadmin/send_records.html', project=project)


@webadmin.route('/submissions/<int:project_id>/reviews/sends/<int:record_id>', methods=['GET', 'POST'])
@superuser
@login_required
def resend_for_review(project_id, record_id):
    project = ProjectRecord.query.get(project_id)
    send_record = ProjectReviewSendRecord.query.get(record_id)
    form = ProjectReviewSendRecordForm(obj=send_record)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_send = ProjectReviewSendRecord()
            form.populate_obj(new_send)
            new_send.to = send_record.to
            new_send.review_id = send_record.review.id
            new_send.sent_at = arrow.now(tz='Asia/Bangkok').datetime,
            db.session.add(new_send)
            db.session.commit()
            serializer = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'), expires_in=1814400)
            token = serializer.dumps({'review_id': send_record.review.id})
            url = url_for('webadmin.write_review',
                          project_id=project.id, review_id=send_record.review.id,
                          token=token, _external=True)
            message = '{}\n\nกรุณาคลิกที่ลิงค์ด้านล่างเพื่อดำเนินการจักเป็นพระคุณยิ่ง\n\n{}\n\nขอความกรุณาส่งผลการประเมินภายในวันที่ {}\n\n{}' \
                .format(form.message.data, url, form.deadline.data.strftime('%d/%m/%Y'), form.footer.data)
            try:
                send_mail(new_send.to, title=form.title.data, message=message)
            except:
                flash('Failed to send an email to {}'.format(new_send.to), 'danger')
            else:
                flash('The request has been resent.', 'success')
            return redirect(url_for('webadmin.view_send_records', project_id=project.id))
    return render_template('webadmin/send_reviews.html', project=project, form=form, to=send_record.to)


@webadmin.route('/submissions/<int:project_id>/reviews/write/<int:review_id>', methods=['GET', 'POST'])
def write_review(project_id, review_id):
    token = request.args.get('token')
    serializer = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'))
    try:
        token_data = serializer.loads(token)
    except:
        return 'Bad JSON Web token. You need a valid token to access this page.'
    if token_data.get('review_id') != review_id:
        return 'Invalid JSON Web Token or the token has expired. Please contact the sender for a valid token to access this page.'
    project = ProjectRecord.query.get(project_id)
    gantt_activities = []
    for a in sorted(project.gantt_activities, key=lambda x: x.task_id):
        gantt_activities.append([
            str(a.task_id),
            GANTT_ACTIVITIES.get(a.task_id),
            a.start_date.isoformat(),
            a.end_date.isoformat(),
            None, 0, None,
            a.start_date,
            a.end_date,
            a.id
        ])
    review = ProjectReviewRecord.query.get(review_id)
    if review.submitted_at:
        return redirect(url_for('webadmin.confirm_review'))
    form = ProjectReviewRecordForm()
    if request.method == 'POST':
        if form.validate_on_submit() and form.confirm_submission.data:
            form.populate_obj(review)
            review.alignment = '|'.join(form.alignment_select.data)
            review.outcome_detail = '|'.join(form.outcome_detail_select.data)
            review.benefit_detail = '|'.join(form.benefit_detail_select.data)
            review.submitted_at = arrow.now(tz='Asia/Bangkok').datetime
            if form.upload_file.data:
                upfile = form.upload_file.data
                filename = secure_filename(upfile.filename)
                upfile.save(filename)
                file_drive = drive.CreateFile({'title': filename})
                file_drive.SetContentFile(filename)
                file_drive.Upload()
                permission = file_drive.InsertPermission({'type': 'anyone',
                                                          'value': 'anyone',
                                                          'role': 'reader'})
                review.file_url = file_drive['id']
            db.session.add(review)
            db.session.commit()

            message = '{} ได้ทำการประเมินและส่งผลการประเมินของโครงการ {} แล้วเมื่อ {}' \
                .format(review.reviewer.fullname, project.title_th, review.submitted_at)

            send_mail(STIN_EMAIL, title='การตอบกลับการรีวิวของผู้ทรงคุณวุฒิ', message=message)

            return redirect(url_for('webadmin.confirm_review'))
        else:
            for e in form.errors:
                flash('{}'.format(e), 'danger')

    return render_template('webadmin/review_form.html',
                           form=form,
                           project=project,
                           review=review,
                           gantt_activities=gantt_activities)


@webadmin.route('/submissions/confirm', methods=['GET', 'POST'])
def confirm_review():
    return render_template('webadmin/review_confirm.html')


@webadmin.route('/submissions/<int:project_id>/status', methods=['GET', 'POST'])
@superuser
@login_required
def update_status(project_id):
    project = ProjectRecord.query.get(project_id)
    prev_status = project.status
    form = ProjectRecordForm(obj=project)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(project)
            project.updated_at = arrow.now(tz='Asia/Bangkok').datetime
            if project.finished or project.terminated or project.rejected:
                project.closed_at = arrow.now('Asia/Bangkok').datetime
            db.session.add(project)
            db.session.commit()
            message = 'เรียนผู้รับผิดชอบโครงการ "{}"\n\nสถานะโครงการได้รับการปรับจาก {} เป็น {} เมื่อ {} นาฬิกา' \
                .format(project.title_th, prev_status, project.status, project.updated_at.strftime('%d/%m/%Y %-H:%M'))
            try:
                send_mail(project.creator.email, title='แจ้งการปรับสถานะโครงการ', message=message)
            except:
                flash('Failed to send an email to the project corresponder.', 'danger')
            flash('Status of the project has been changed.', 'success')
            return redirect(url_for('webadmin.submission_detail', project_id=project.id))

    return render_template('webadmin/status.html', project=project, form=form)


@webadmin.route('/ethics')
@superuser
@login_required
def list_ethics():
    ethics = ProjectEthicRecord.query.all()
    return render_template('webadmin/ethics.html', ethics=ethics)


@webadmin.route('/ethics/<int:ethic_id>')
@superuser
@login_required
def ethic_detail(ethic_id):
    ethic = ProjectEthicRecord.query.get(ethic_id)
    return render_template('webadmin/ethic_detail.html', ethic=ethic, project=ethic.project)


@webadmin.route('/ethics/<int:ethic_id>/update', methods=['GET', 'POST'])
@superuser
@login_required
def update_ethic_status(ethic_id):
    ethic = ProjectEthicRecord.query.get(ethic_id)
    form = ProjectEthicRecordForm(obj=ethic)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(ethic)
            ethic.updated_at = arrow.now(tz='Asia/Bangkok').datetime,
            db.session.add(ethic)
            db.session.commit()
            flash('The ethic status has been updated.', 'success')
            return redirect(url_for('webadmin.ethic_detail', ethic_id=ethic.id))
    return render_template('webadmin/update_ethic.html', ethic=ethic, form=form)


@webadmin.route('/<int:project_id>/ethic/<int:ethic_id>/reviewers/add')
@superuser
@login_required
def list_ethic_reviewers(project_id, ethic_id):
    project = ProjectRecord.query.get(project_id)
    groups = ProjectReviewerGroup.query.all()
    ethic = ProjectEthicRecord.query.get(ethic_id)
    return render_template('webadmin/ethic_reviewers_add.html', project=project, groups=groups, ethic=ethic)


@webadmin.route('/ethics/<int:ethic_id>/reviewers/add/<int:reviewer_id>')
@superuser
@login_required
def add_ethic_reviewer(ethic_id, reviewer_id):
    review = ProjectEthicReviewRecord.query.filter_by(reviewer_id=reviewer_id,
                                                      ethic_id=ethic_id).first()
    if not review:
        review = ProjectEthicReviewRecord(
            ethic_id=ethic_id,
            reviewer_id=reviewer_id
        )
        db.session.add(review)
        db.session.commit()
        flash('Reviewer has been added to the ethic review board.', 'success')
    return redirect(request.referrer)


@webadmin.route('/ethics/<int:ethic_id>/reviewers/add/all/<int:group_id>')
@superuser
@login_required
def add_all_ethic_reviewers(ethic_id, group_id):
    reviewer_group = ProjectReviewerGroup.query.get(group_id)
    ethic = ProjectEthicRecord.query.get(ethic_id)
    for reviewer in reviewer_group.reviewers:
        if reviewer not in ethic.reviewers:
            review = ProjectEthicReviewRecord(reviewer=reviewer, ethic=ethic)
            db.session.add(review)
    db.session.commit()
    flash('All reviewers have been added to the ethic review board.', 'success')
    return redirect(request.referrer)


@webadmin.route('/ethics/<int:ethic_id>/reviewers/remove/<int:reviewer_id>')
@superuser
@login_required
def remove_ethic_reviewer(ethic_id, reviewer_id):
    review = ProjectEthicReviewRecord.query.filter_by(reviewer_id=reviewer_id,
                                                      ethic_id=ethic_id).first()
    if review:
        db.session.delete(review)
        db.session.commit()
        flash('Reviewer has been removed to the project review.', 'success')
    else:
        flash('Reviewer not found in the project review.', 'warning')
    return redirect(request.referrer)


@webadmin.route('/ethics/<int:ethic_id>/reviewers/remove/all')
@superuser
@login_required
def remove_all_ethic_reviewers(ethic_id):
    ethic = ProjectEthicRecord.query.get(ethic_id)
    for review in ethic.reviews:
        db.session.delete(review)
        db.session.commit()
    flash('All reviewers have been removed to the project review.', 'success')
    return redirect(request.referrer)


@webadmin.route('/submissions/<int:project_id>/ethics/<int:ethic_id>/reviews/send',
                methods=['GET', 'POST'])
@superuser
@login_required
def send_for_ethic_reviews(project_id, ethic_id):
    project = ProjectRecord.query.get(project_id)
    ethic = ProjectEthicRecord.query.get(ethic_id)
    form = ProjectEthicReviewSendRecordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            for review in ethic.reviews:
                serializer = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'), expires_in=1814400)
                token = serializer.dumps({'review_id': review.id})
                url = url_for('webadmin.write_ethic_review', project_id=project.id, review_id=review.id, token=token,
                              _external=True)
                message = '{}\n\nกรุณาคลิกที่ลิงค์ด้านล่างเพื่อดำเนินการจักเป็นพระคุณยิ่ง\n\n{}\n\nขอความกรุณาส่งผลการประเมินภายในวันที่ {}\n\n{}' \
                    .format(form.message.data, url, form.deadline.data.strftime('%d/%m/%Y'), form.footer.data)
                try:
                    send_mail(review.reviewer.email, title=form.title.data, message=message)
                except:
                    flash('Failed to send an email to {}'.format(review.reviewer.email), 'danger')
                else:
                    new_send = ProjectEthicReviewSendRecord()
                    form.populate_obj(new_send)
                    new_send.review_id = review.id
                    new_send.to = review.reviewer.email
                    new_send.sent_at = arrow.now(tz='Asia/Bangkok').datetime,
                    db.session.add(new_send)
            db.session.commit()
            flash('The project has been sent for a review.', 'success')
            return redirect(url_for('webadmin.ethic_detail', project_id=project.id, ethic_id=ethic_id))
    return render_template('webadmin/send_reviews.html', form=form, project=project)


@webadmin.route('/submissions/<int:project_id>/ethics/<int:ethic_id>/reviews/sends', methods=['GET', 'POST'])
@superuser
@login_required
def view_send_ethic_records(project_id, ethic_id):
    project = ProjectRecord.query.get(project_id)
    ethic = ProjectEthicRecord.query.get(ethic_id)
    return render_template('webadmin/send_ethic_records.html', project=project, ethic=ethic)


@webadmin.route('/submissions/<int:project_id>/ethics/<int:ethic_id>/reviews/sends/<int:record_id>',
                methods=['GET', 'POST'])
@superuser
@login_required
def resend_for_ethic_review(project_id, record_id, ethic_id):
    project = ProjectRecord.query.get(project_id)
    send_record = ProjectEthicReviewSendRecord.query.get(record_id)
    form = ProjectEthicReviewSendRecordForm(obj=send_record)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_send = ProjectEthicReviewSendRecord()
            new_send.sent_at = arrow.now(tz='Asia/Bangkok').datetime,
            form.populate_obj(new_send)
            new_send.to = send_record.to
            new_send.review_id = send_record.review.id
            db.session.add(new_send)
            db.session.commit()
            serializer = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'), expires_in=1814400)
            token = serializer.dumps({'review_id': send_record.review.id})
            url = url_for('webadmin.write_ethic_review',
                          project_id=project.id, review_id=send_record.review.id,
                          ethic_id=ethic_id, token=token, _external=True)
            message = '{}\n\nกรุณาคลิกที่ลิงค์ด้านล่างเพื่อดำเนินการจักเป็นพระคุณยิ่ง\n\n{}\n\nขอความกรุณาส่งผลการประเมินภายในวันที่ {}\n\n{}' \
                .format(form.message.data, url, form.deadline.data.strftime('%d/%m/%Y'), form.footer.data)
            try:
                send_mail(new_send.to, title=form.title.data, message=message)
            except:
                flash('Failed to send an email to {}'.format(send_record.review.reviewer.email), 'danger')
            flash('The request has been resent to {}.'.format(new_send.to), 'success')
            return redirect(url_for('webadmin.view_send_ethic_records',
                                    project_id=project.id, ethic_id=ethic_id))
    return render_template('webadmin/send_reviews.html',
                           project=project, form=form, to=send_record.to)


@webadmin.route('/submissions/<int:project_id>/ethics/<int:ethic_id>/reviews/<int:review_id>/add',
                methods=['GET', 'POST'])
def write_ethic_review(project_id, ethic_id, review_id):
    project = ProjectRecord.query.get(project_id)
    review = ProjectEthicReviewRecord.query.get(review_id)
    token = request.args.get('token')
    serializer = TimedJSONWebSignatureSerializer(os.environ.get('SECRET_KEY'))
    try:
        token_data = serializer.loads(token)
    except:
        return 'Bad JSON Web token. You need a valid token to access this page.'
    if token_data.get('review_id') != review_id:
        return 'Invalid JSON Web Token or the token has expired. Please contact the sender for a valid token to access this page.'
    if review.submitted_at:
        return redirect(url_for('webadmin.confirm_review'))

    form = ProjectEthicReviewRecordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(review)
            review.submitted_at = arrow.now(tz='Asia/Bangkok').datetime
            db.session.add(review)
            db.session.commit()
            return redirect(url_for('webadmin.confirm_review'))

    return render_template('webadmin/ethic_review_form.html', form=form, project=project, review=review)


@webadmin.route('/submissions/<int:project_id>/ethics/<int:ethic_id>/reviews')
@superuser
@login_required
def view_ethic_reviews(project_id, ethic_id):
    project = ProjectRecord.query.get(project_id)
    ethic = ProjectEthicRecord.query.get(ethic_id)
    return render_template('webadmin/ethic_reviews.html',
                           project=project, ethic=ethic)


@webadmin.route('/pubs/add', methods=['GET', 'POST'])
@superuser
@login_required
def add_pub():
    form = ProjectPublicationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_pub = ProjectPublication()
            form.populate_obj(new_pub)
            new_pub.journal = form.journals.data
            db.session.add(new_pub)
            db.session.commit()
            flash('New publication added.', 'success')
            return redirect(url_for('webadmin.add_pub_author', pub_id=new_pub.id))
        else:
            flash(form.errors, 'danger')
        return redirect(url_for('webadmin.add_pub'))
    return render_template('webadmin/pub_add.html', form=form)


@webadmin.route('/journals/add', methods=['GET', 'POST'])
@superuser
@login_required
def add_journal():
    form = ProjectJournalForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_journal = ProjectPublicationJournal()
            form.populate_obj(new_journal)
            db.session.add(new_journal)
            db.session.commit()
            flash('New journal added.', 'success')
            return redirect(url_for('webadmin.add_pub'))
        else:
            flash(form.errors, 'danger')
    return render_template('webadmin/journal_add.html', form=form)


@webadmin.route('/pubs')
@superuser
@login_required
def list_pubs():
    pubs = ProjectPublication.query.all()
    return render_template('webadmin/pubs.html',
                           pubs=sorted(pubs, key=lambda x: x.pub_date, reverse=True))


@webadmin.route('/pubs/<int:pub_id>')
@superuser
@login_required
def show_pub(pub_id):
    pub = ProjectPublication.query.get(pub_id)
    return render_template('webadmin/pub_detail.html', pub=pub)


@webadmin.route('/pubs/<int:pub_id>/edit', methods=['GET', 'POST'])
@superuser
@login_required
def edit_pub(pub_id):
    pub = ProjectPublication.query.get(pub_id)
    form = ProjectPublicationForm(obj=pub)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(pub)
            db.session.add(pub)
            db.session.commit()
            flash('Data have been saved.', 'success')
            return redirect(url_for('webadmin.list_pubs'))
        else:
            flash(form.errors, 'danger')
    return render_template('webadmin/pub_edit.html', form=form, pub=pub)


@webadmin.route('projects/pubs/<int:pub_id>/remove', methods=['GET', 'POST'])
@superuser
@login_required
def remove_pub(pub_id):
    pub = ProjectPublication.query.get(pub_id)
    confirm = request.args.get('confirm', 'no')
    if confirm == 'yes':
        if pub:
            db.session.delete(pub)
            db.session.commit()
            flash('Data have been removed.', 'success')
            return redirect(url_for('webadmin.list_pubs'))
        else:
            flash('Publication no longer exists.', 'warning')
    return render_template('webadmin/pub_remove.html', pub=pub)


@webadmin.route('/pubs/<int:pub_id>/authors/edit', methods=['GET', 'POST'])
@superuser
@login_required
def edit_pub_authors(pub_id):
    pub = ProjectPublication.query.get(pub_id)
    return render_template('webadmin/pub_author_edit.html', pub=pub)


@webadmin.route('/pubs/<int:pub_id>/authors/add', methods=['GET', 'POST'])
@superuser
@login_required
def add_pub_author(pub_id):
    pub = ProjectPublication.query.get(pub_id)
    form = ProjectPublicationAuthorForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_author = ProjectPublicationAuthor()
            form.populate_obj(new_author)
            new_author.pub = pub
            new_author.user = form.users.data
            db.session.add(new_author)
            db.session.commit()
            flash('New author has been added.', 'success')
            return redirect(url_for('webadmin.edit_pub_authors', pub_id=pub_id))
        else:
            flash(form.errors, 'danger')
    return render_template('webadmin/pub_author_add.html', pub=pub, form=form)


@webadmin.route('/pubs/<int:pub_id>/authors/<int:author_id>/remove', methods=['GET', 'POST'])
@superuser
@login_required
def remove_pub_author(pub_id, author_id):
    author = ProjectPublicationAuthor.query.get(author_id)
    if author:
        db.session.delete(author)
        db.session.commit()
        flash('Author has been deleted from publication', 'success')
    else:
        flash('The author with that ID was not found.', 'danger', )
    return redirect(url_for('webadmin.edit_pub_authors', pub_id=pub_id))


@webadmin.route('/users')
@superuser
@login_required
def list_users():
    users = User.query.all()
    return render_template('webadmin/users.html', users=users)


@webadmin.route('/support/lang-edit/requests')
@superuser
@login_required
def list_lang_edit_requests():
    requests = ProjectLanguageEditingSupport.query.all()
    return render_template('webadmin/lang_edit_list.html', requests=requests)


@webadmin.route('/pubs/<int:pub_id>/support/language/<int:record_id>/edit', methods=['GET', 'POST'])
@superuser
@login_required
def edit_lang_support(pub_id, record_id):
    record = ProjectLanguageEditingSupport.query.get(record_id)
    form = ProjectLanguageEditSupportForm(obj=record)
    criteria = record.criteria.split('|')
    qualification = record.qualification.split('|')
    docs = record.docs.split('|')
    request_data = record.request.split('|')
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(record)
            record.qualification = '|'.join(form.qualification_select.data)
            record.criteria = '|'.join(form.criteria_select.data)
            record.docs = '|'.join(form.docs_select.data)
            record.request = '|'.join(form.request_select.data)
            record.edited_at = arrow.now(tz='Asia/Bangkok').datetime,
            if record.status == 'อนุมัติ':
                record.approved_at = arrow.now(tz='Asia/Bangkok').datetime
            db.session.add(record)
            db.session.commit()
            flash('The language edit request has been edited.', 'success')
            return redirect(url_for('webadmin.list_lang_edit_requests'))
        else:
            flash(form.errors, 'danger')
    return render_template('webadmin/lang_support_edit.html',
                           form=form,
                           docs=docs, request_data=request_data,
                           qualification=qualification, criteria=criteria)


@webadmin.route('/support/rewards')
@superuser
@login_required
def list_pub_rewards():
    rewards = ProjectPublishedReward.query.all()
    return render_template('webadmin/rewards_list.html', rewards=rewards)


@webadmin.route('/pubs/<int:pub_id>/support/reward/<int:record_id>/edit', methods=['GET', 'POST'])
@superuser
@login_required
def edit_pub_reward(pub_id, record_id):
    pub = ProjectPublication.query.get(pub_id)
    record = ProjectPublishedReward.query.get(record_id)
    qualification = record.qualification.split('|')
    form = ProjectPublishedRewardForm(obj=record)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(record)
            record.qualification = '|'.join(form.qualification_select.data)
            record.edited_at = arrow.now(tz='Asia/Bangkok').datetime
            if record.status == 'อนุมัติ':
                record.approved_at = arrow.now(tz='Asia/Bangkok').datetime
            if record.reward:
                reward_amt = float(record.reward.split()[-2])
            else:
                reward_amt = 0.0
            if record.apc:
                apc_amt = float(record.apc.split()[-2])
            else:
                apc_amt = 0.0
            record.amount = reward_amt + apc_amt
            db.session.add(record)
            db.session.commit()
            flash('The publication reward/fee request has been edited.', 'success')
            return redirect(url_for('webadmin.list_pub_rewards'))
        else:
            flash(form.errors, 'danger')
    return render_template('webadmin/reward_edit.html',
                           record=record, form=form,
                           pub=pub, qualification=qualification)


@webadmin.route('/dashboard')
@superuser
@login_required
def dashboard():
    projstat = defaultdict(int)
    for project in ProjectRecord.query.all():
        projstat[project.status] += 1
    project_status = [(k, v) for k, v in projstat.items()]
    project_status = [('Status', 'Count')] + project_status

    df = pd.read_sql_query('select * from projects;', con=db.engine)
    per_month = df.created_at.dt.to_period('M')
    per_month_counts = df.groupby([per_month, 'status']).count()
    per_month_count_dict = per_month_counts['id'].to_dict()
    months = per_month_count_dict.keys()
    all_status = set()
    for m in months:
        all_status.add(m[1])
    all_status = list(all_status)
    all_status_dict = dict(list(zip(all_status, range(len(all_status)))))
    per_month_count_data = {}
    for k in months:
        month_data = [0] * len(all_status)
        label = '{}/{}'.format(k[0].month, k[0].year)
        per_month_count_data[label] = month_data

    for k in months:
        label = '{}/{}'.format(k[0].month, k[0].year)
        cnt = per_month_count_dict[k]
        idx = all_status_dict[k[1]]
        per_month_count_data[label][idx] = cnt

    labels = ['Month'] + all_status
    per_month_count_data_list = [labels]
    for k, v in per_month_count_data.items():
        v.insert(0, k)
        per_month_count_data_list.append(v)

    reward_df = pd.read_sql_query('select * from project_pub_rewards;', con=db.engine)
    per_month = reward_df.submitted_at.dt.to_period('M')
    per_month_count = reward_df.groupby([per_month]).sum().amount
    reward_sum_data = [['Month', 'Total']]
    for mnt, total in per_month_count.to_dict().items():
        label = '{}/{}'.format(mnt.month, mnt.year)
        reward_sum_data.append([label, total])
    month_names = dict(list(zip(['January', 'February', 'March', 'April', 'May',
                                 'June', 'July', 'August', 'September',
                                 'October', 'November', 'December'], range(1, 13))))

    pub_df = pd.read_sql_query('select * from project_pub_records', con=db.engine)
    pub_month_data = pub_df.groupby(['year', 'month']).count().id.reset_index()
    pub_month_data_list = [['Month', 'Count']]
    for idx, row in pub_month_data.iterrows():
        label = '{}/{}'.format(month_names.get(row[1], ''), row[0])
        pub_month_data_list.append([label, row[2]])

    return render_template('webadmin/dashboard.html',
                           project_status=project_status,
                           project_per_month_count_data=per_month_count_data_list,
                           reward_sum_data=reward_sum_data,
                           pub_month_data=pub_month_data_list)


@webadmin.route('/intl-conference/supports')
@superuser
@login_required
def list_intl_conference_supports():
    return render_template('webadmin/intl_conference_support_list.html')


@webadmin.route('/intl-conference/supports/<int:request_id>', methods=['GET', 'POST'])
@superuser
@login_required
def edit_intl_conference_support(request_id):
    req = IntlConferenceSupport.query.get(request_id)
    if req:
        qualification = req.qualification.split('|')
        form = IntlConferenceSupportForm(obj=req)
        if request.method == 'POST' and form.validate_on_submit():
            form.populate_obj(req)
            req.qualification = '|'.join(form.qualification_select.data)
            req.edited_at = arrow.now(tz='Asia/Bangkok').datetime,
            db.session.add(req)
            db.session.commit()
            flash('The request has been updated.', 'success')
            return redirect(url_for('webadmin.list_intl_conference_supports'))
    return render_template('webadmin/intl_conference_support_edit.html',
                           form=form, qualification=qualification, request_id=req.id)


@webadmin.route('/proposal-development/supports')
@superuser
@login_required
def list_proposal_development_supports():
    supports = ProjectProposalDevelopmentSupport.query.all()
    return render_template('webadmin/proposal_development_support_list.html', supports=supports)


@webadmin.route('/proposal-development/supports/<int:request_id>',
                methods=['GET', 'POST'])
@superuser
@login_required
def edit_proposal_development_support(request_id):
    req = ProjectProposalDevelopmentSupport.query.get(request_id)
    if req:
        qualification = req.qualification.split('|')
        docs = req.docs.split('|')
        form = ProjectProposalDevelopmentSupportForm(obj=req)
        qualification = req.qualification.split('|')
        if request.method == 'POST' and form.validate_on_submit():
            form.populate_obj(req)
            req.qualification = '|'.join(form.qualification_select.data)
            req.docs = '|'.join(form.docs_select.data)
            req.edited_at = arrow.now(tz='Asia/Bangkok').datetime,
            if form.contract_upload.data:
                upfile = form.contract_upload.data
                filename = secure_filename(upfile.filename)
                upfile.save(filename)
                file_drive = drive.CreateFile({'title': filename})
                file_drive.SetContentFile(filename)
                file_drive.Upload()
                permission = file_drive.InsertPermission({'type': 'anyone',
                                                          'value': 'anyone',
                                                          'role': 'reader'})
                req.contract_file_url = file_drive['id']
            db.session.add(req)
            db.session.commit()
            flash('The request has been updated.', 'success')
            return redirect(url_for('webadmin.list_proposal_development_supports'))
    return render_template('webadmin/proposal_development_support_edit.html',
                           form=form, qualification=qualification, docs=docs,
                           contract_url=req.contract_file_url,
                           request_id=req.id)


@webadmin.route('/proposal-development/supports/<int:request_id>/approve')
@superuser
@login_required
def approve_proposal_development_support(request_id):
    req = ProjectProposalDevelopmentSupport.query.get(request_id)
    if req:
        req.approved_at = arrow.now(tz='Asia/Bangkok').datetime,
        db.session.add(req)
        db.session.commit()
        flash('The request has been approved.', 'success')
        return redirect(url_for('webadmin.list_proposal_development_supports'))


@webadmin.route('/intl-conference/supports/<int:request_id>/approve')
@superuser
@login_required
def approve_intl_conference_support(request_id):
    req = IntlConferenceSupport.query.get(request_id)
    if req:
        req.approved_at = arrow.now(tz='Asia/Bangkok').datetime,
        db.session.add(req)
        db.session.commit()
        flash('The request has been approved.', 'success')
        return render_template('webadmin/intl_conference_support_list.html')


@webadmin.route('/projects')
def list_projects():
    projects = ProjectRecord.query.all()
    return render_template('webadmin/all_projects.html', projects=projects)


@webadmin.route('/projects/<int:project_id>/detail')
@superuser
@login_required
def display_detail(project_id):
    project = ProjectRecord.query.get(project_id)
    gantt_activities = []
    for a in sorted(project.gantt_activities, key=lambda x: x.task_id):
        gantt_activities.append([
            str(a.task_id),
            GANTT_ACTIVITIES.get(a.task_id),
            a.start_date.isoformat(),
            a.end_date.isoformat(),
            None, 0, None,
            a.start_date,
            a.end_date,
            a.id
        ])
    return render_template('webadmin/detail.html',
                           project=project,
                           gantt_activities=gantt_activities
                           )


@webadmin.route('/progress-reports')
@superuser
@login_required
def list_progress_reports():
    milestone_query = ProjectMilestone.query.filter(ProjectMilestone.submitted_at != None) \
        .filter_by(received_at=None).order_by(ProjectMilestone.created_at.desc())
    return render_template('webadmin/progress_reports.html', milestones=milestone_query)


@webadmin.route('/close-project-requests')
@superuser
@login_required
def close_project_requests():
    projects = ProjectRecord.query.filter(ProjectRecord.close_requested_at != None) \
        .filter(ProjectRecord.closed_at == None).all()
    return render_template('webadmin/close_requests.html', requests=projects)


@webadmin.route('/progress-reports/<int:milestone_id>/receive')
@superuser
@login_required
def receive_a_progress(milestone_id):
    milestone = ProjectMilestone.query.get(milestone_id)
    if not milestone.received_at:
        milestone.received_at = arrow.now(tz='Asia/Bangkok').datetime
        db.session.add(milestone)
        db.session.commit()
        try:
            message = 'เรียนผู้รับผิดชอบโครงการ{}'.format(milestone.project.title_th)
            message += '\n\nศูนย์วิจัยได้รับรายงานความก้าวหน้าของท่านที่ส่งเมื่อวันที่ {} เรียบร้อยแล้ว' \
                .format(milestone.submitted_at.strftime('%d/%m/%Y %H:%M:%S'))
            send_mail(milestone.project.creator.email, 'แจ้งรับรายงานความก้าวหน้าโครงการฯ', message)
        except:
            flash('Failed to send an email notification', 'danger')
        flash('บันทึกข้อมูลเรียบร้อยแล้ว', 'success')
    return redirect(url_for('webadmin.list_progress_reports'))


@webadmin.route('/progress-reports/<int:milestone_id>/gantt-chart')
@superuser
@login_required
def list_gantt_activity(milestone_id):
    milestone = ProjectMilestone.query.get(milestone_id)
    gantt_activities = []
    for a in sorted(milestone.gantt_activities, key=lambda x: x.task_id):
        gantt_activities.append([
            str(a.task_id),
            GANTT_ACTIVITIES.get(a.task_id),
            a.start_date.isoformat(),
            a.end_date.isoformat(),
            None, float(a.completion), None
        ])
    return render_template('webadmin/gantt_activities.html',
                           milestone=milestone, gantt_activities=gantt_activities)


@webadmin.route('/progress-reports/<int:milestone_id>/budgets')
@superuser
@login_required
def list_budgets(milestone_id):
    milestone = ProjectMilestone.query.get(milestone_id)
    return render_template('webadmin/budgets.html', milestone=milestone)


@webadmin.route('/progress-reports/<int:milestone_id>/summaries')
@superuser
@login_required
def list_summaries(milestone_id):
    milestone = ProjectMilestone.query.get(milestone_id)
    return render_template('webadmin/progress_summaries.html', milestone=milestone)


@webadmin.route('/progress-reports/<int:milestone_id>/send-to-committee')
@superuser
@login_required
def send_progress_to_committee(milestone_id):
    milestone = ProjectMilestone.query.get(milestone_id)
    for reviewer in milestone.project.reviewers:
        message = 'เรียนคณะกรรมการโครงการวิจัย'
        message += '\n\nโครงการ{} ได้ทำการส่งรายงานความก้าวหน้าเมื่อวันที่{}\n\nกรุณาคลิกที่ลิงค์ด้านล่างเพื่อตรวจสอบรายงานความก้าวหน้าจักเป็นพระคุณยิ่ง\n\n{}' \
            .format(milestone.project.title_th, milestone.submitted_at.strftime('%d/%m/%Y %H:%M:%S'),
                    url_for('webadmin.display_progress_report_committee', milestone_id=milestone_id, _external=True))
        try:
            send_mail(reviewer.email, title='รายงานความก้าวหน้าโครงการวิจัย', message=message)
        except:
            flash('Failed to send an email to {}'.format(reviewer.email))
    return 'Progress sent.'


@webadmin.route('/progress-reports/<int:milestone_id>/committee')
def display_progress_report_committee(milestone_id):
    milestone = ProjectMilestone.query.get(milestone_id)
    gantt_activities = []
    for a in sorted(milestone.gantt_activities, key=lambda x: x.task_id):
        gantt_activities.append([
            str(a.task_id),
            GANTT_ACTIVITIES.get(a.task_id),
            a.start_date.isoformat(),
            a.end_date.isoformat(),
            None, float(a.completion), None
        ])
    return render_template('webadmin/progress_report_committee.html',
                           milestone=milestone, gantt_activities=gantt_activities)


@webadmin.route('/academic-supports')
@superuser
def academic_support_index():
    return render_template('webadmin/academic_support_index.html')


@webadmin.route('/academic-supports/development-types', methods=['GET', 'POST'])
@superuser
def manage_development_types():
    form = DevelopmentTypeForm()
    if form.validate_on_submit():
        new_type = DevelopmentType()
        form.populate_obj(new_type)
        db.session.add(new_type)
        db.session.commit()
        flash('New development type has been added.', 'success')
        return redirect(url_for('webadmin.manage_development_types'))
    dev_types = DevelopmentType.query.all()
    return render_template('webadmin/development_types.html', dev_types=dev_types, form=form)


@webadmin.route('/academic-supports/development-types/<int:dev_type_id>', methods=['GET', 'POST'])
@superuser
def edit_development_type(dev_type_id):
    t = DevelopmentType.query.get(dev_type_id)
    form = DevelopmentTypeForm(obj=t)
    if form.validate_on_submit():
        form.populate_obj(t)
        db.session.add(t)
        db.session.commit()
        flash('New development type has been added.', 'success')
    return render_template('webadmin/edit_development_type.html', form=form, t=t)


@webadmin.route('/academic-supports/development-types/<int:dev_type_id>/delete')
@superuser
def delete_development_type(dev_type_id):
    t = DevelopmentType.query.get(dev_type_id)
    if t:
        db.session.delete(t)
        db.session.commit()
        flash('The development type has been deleted.', 'success')
    return redirect(url_for('webadmin.manage_development_types'))


@webadmin.route('/academic-supports/development-categories', methods=['GET', 'POST'])
@superuser
def manage_development_categories():
    form = DevelopmentCategoryForm()
    if form.validate_on_submit():
        new_cat = DevelopmentCategory()
        form.populate_obj(new_cat)
        db.session.add(new_cat)
        db.session.commit()
        flash('New development category has been added.', 'success')
        return redirect(url_for('webadmin.manage_development_categories'))
    dev_cats = DevelopmentCategory.query.all()
    return render_template('webadmin/development_categories.html', dev_cats=dev_cats, form=form)


@webadmin.route('/academic-supports/development-categories/<int:dev_cat_id>', methods=['GET', 'POST'])
@superuser
def edit_development_category(dev_cat_id):
    c = DevelopmentCategory.query.get(dev_cat_id)
    form = DevelopmentCategoryForm(obj=c)
    if form.validate_on_submit():
        form.populate_obj(c)
        db.session.add(c)
        db.session.commit()
        flash('New development category has been added.', 'success')
    return render_template('webadmin/edit_development_category.html', form=form, c=c)


@webadmin.route('/academic-supports/development-categories/<int:dev_cat_id>/delete')
@superuser
def delete_development_category(dev_cat_id):
    t = DevelopmentCategory.query.get(dev_cat_id)
    if t:
        db.session.delete(t)
        db.session.commit()
        flash('The development category has been deleted.', 'success')
    return redirect(url_for('webadmin.manage_development_categories'))


@webadmin.route('/academic-supports/development-requests')
@superuser
def manage_development_requests():
    dev_requests = DevelopmentRecord.query.filter(DevelopmentRecord.approved_at.is_(None)).\
        filter(DevelopmentRecord.rejected_at.is_(None))
    return render_template('webadmin/development_support_requests.html', dev_requests=dev_requests)


@webadmin.route('/academic-supports/development-requests/<int:req_id>')
@superuser
def view_development_request(req_id):
    rec = DevelopmentRecord.query.get(req_id)
    return render_template('webadmin/development_request_detail.html', rec=rec)


@webadmin.route('/academic-supports/development-requests/<int:req_id>/update-status')
@superuser
def approve_development_request(req_id):
    rec = DevelopmentRecord.query.get(req_id)
    status = request.args.get('status')
    if status == 'approve':
        rec.approved_at = arrow.now(tz='Asia/Bangkok').datetime
    elif status == 'reject':
        rec.rejected_at = arrow.now(tz='Asia/Bangkok').datetime
    db.session.add(rec)
    db.session.commit()
    return redirect(url_for('webadmin.view_development_request', req_id=rec.id))
