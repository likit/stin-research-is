import arrow
from app.webadmin import webadmin_bp as webadmin
from wsgi import db
from flask import render_template, redirect, url_for, request, flash
from app.project.models import (ProjectRecord, ProjectReviewerGroup,
                                ProjectReviewSendRecord, ProjectReviewRecord,
                                ProjectEthicRecord, ProjectEthicReviewRecord,
                                ProjectEthicReviewSendRecord, ProjectPublicationJournal,
                                ProjectPublication,
                                )
from app.webadmin.forms import (ProjectReviewSendRecordForm, ProjectReviewRecordForm,
                                ProjectEthicReviewSendRecordForm, ProjectEthicReviewRecordForm
                                )
from app.project.forms import ProjectRecordForm, ProjectPublicationForm, ProjectJournalForm


@webadmin.route('/submissions')
def list_submissions():
    submissions = ProjectRecord.query.filter_by(status='submitted')
    return render_template('webadmin/submissions.html', submissions=submissions)


@webadmin.route('/submissions/<int:project_id>')
def submission_detail(project_id):
    project = ProjectRecord.query.get(project_id)
    return render_template('webadmin/submission_detail.html', project=project)


@webadmin.route('/submissions/<int:project_id>/reviewers/add')
def list_reviewers(project_id):
    project = ProjectRecord.query.get(project_id)
    groups = ProjectReviewerGroup.query.all()
    return render_template('webadmin/reviewers_add.html',
                           project=project,
                           groups=groups)


@webadmin.route('/submissions/<int:project_id>/reviewers/add/<int:reviewer_id>')
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
def remove_reviewer(project_id, reviewer_id):
    review = ProjectReviewRecord.query.filter_by(reviewer_id=reviewer_id,
                                                 project_id=project_id).first()
    db.session.delete(review)
    db.session.commit()
    flash('Reviewer has been removed to the project review.', 'success')
    return redirect(request.referrer)


@webadmin.route('/submissions/<int:project_id>/reviewers/remove/all')
def remove_all_reviewers(project_id):
    project = ProjectRecord.query.get(project_id)
    for review in project.reviews:
        db.session.delete(review)
        db.session.commit()
    flash('All reviewers have been removed to the project review.', 'success')
    return redirect(request.referrer)


@webadmin.route('/submissions/<int:project_id>/reviews')
def view_reviews(project_id):
    project = ProjectRecord.query.get(project_id)
    return render_template('webadmin/reviews.html', project=project)


@webadmin.route('/submissions/<int:project_id>/reviews/send', methods=['GET', 'POST'])
def send_for_reviews(project_id):
    project = ProjectRecord.query.get(project_id)
    form = ProjectReviewSendRecordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            for review in project.reviews:
                new_send = ProjectReviewSendRecord()
                form.populate_obj(new_send)
                new_send.review_id = review.id
                new_send.to = review.reviewer.email
                new_send.sent_at = arrow.now(tz='Asia/Bangkok').datetime,
                db.session.add(new_send)
            db.session.commit()
            flash('The project has been sent for a review.')
            return redirect(url_for('webadmin.submission_detail', project_id=project.id))
    return render_template('webadmin/send_reviews.html', form=form, project=project)


@webadmin.route('/submissions/<int:project_id>/reviews/sends', methods=['GET', 'POST'])
def view_send_records(project_id):
    project = ProjectRecord.query.get(project_id)
    return render_template('webadmin/send_records.html', project=project)


@webadmin.route('/submissions/<int:project_id>/reviews/sends/<int:record_id>', methods=['GET', 'POST'])
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
            flash('The request has been resent.', 'success')
            return redirect(url_for('webadmin.view_send_records', project_id=project.id))
    return render_template('webadmin/send_reviews.html', project=project, form=form, to=send_record.to)


@webadmin.route('/submissions/<int:project_id>/reviews/write/<int:review_id>', methods=['GET', 'POST'])
def write_review(project_id, review_id):
    project = ProjectRecord.query.get(project_id)
    review = ProjectReviewRecord.query.get(review_id)
    if review.submitted_at:
        return redirect(url_for('webadmin.confirm_review'))
    form = ProjectReviewRecordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(review)
            review.submitted_at = arrow.now(tz='Asia/Bangkok').datetime
            db.session.add(review)
            db.session.commit()
            return redirect(url_for('webadmin.confirm_review'))

    return render_template('webadmin/review_form.html', form=form, project=project, review=review)


@webadmin.route('/submissions/confirm', methods=['GET', 'POST'])
def confirm_review():
    return render_template('webadmin/review_confirm.html')


@webadmin.route('/submissions/<int:project_id>/status', methods=['GET', 'POST'])
def update_status(project_id):
    project = ProjectRecord.query.get(project_id)
    form = ProjectRecordForm(obj=project)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(project)
            project.updated_at = arrow.now(tz='Asia/Bangkok').datetime
            db.session.add(project)
            db.session.commit()
            flash('Status of the project has been changed.', 'success')
            return redirect(url_for('webadmin.submission_detail', project_id=project.id))

    return render_template('webadmin/status.html', project=project, form=form)


@webadmin.route('/ethics')
def list_ethics():
    ethics = ProjectEthicRecord.query.all()
    return render_template('webadmin/ethics.html', ethics=ethics)


@webadmin.route('/ethics/<int:ethic_id>')
def ethic_detail(ethic_id):
    ethic = ProjectEthicRecord.query.get(ethic_id)
    return render_template('webadmin/ethic_detail.html', ethic=ethic, project=ethic.project)


@webadmin.route('/project/<int:project_id>/ethic/<int:ethic_id>/reviewers/add')
def list_ethic_reviewers(project_id, ethic_id):
    project = ProjectRecord.query.get(project_id)
    groups = ProjectReviewerGroup.query.all()
    ethic = ProjectEthicRecord.query.get(ethic_id)
    return render_template('webadmin/ethic_reviewers_add.html', project=project, groups=groups, ethic=ethic)


@webadmin.route('/ethics/<int:project_id>/reviewers/add/<int:reviewer_id>')
def add_ethic_reviewer(project_id, reviewer_id):
    review = ProjectEthicReviewRecord.query.filter_by(reviewer_id=reviewer_id,
                                                      project_id=project_id).first()
    if not review:
        review = ProjectEthicReviewRecord(
            project_id=project_id,
            reviewer_id=reviewer_id
        )
        db.session.add(review)
        db.session.commit()
        flash('Reviewer has been added to the ethic review board.', 'success')
    return redirect(request.referrer)


@webadmin.route('/ethics/<int:project_id>/reviewers/add/all/<int:group_id>')
def add_all_ethic_reviewers(project_id, group_id):
    reviewer_group = ProjectReviewerGroup.query.get(group_id)
    project = ProjectRecord.query.get(project_id)
    for reviewer in reviewer_group.reviewers:
        if reviewer not in project.ethic_reviewers:
            review = ProjectEthicReviewRecord(reviewer=reviewer, project=project)
            db.session.add(review)
    db.session.commit()
    flash('All reviewers have been added to the ethic review board.', 'success')
    return redirect(request.referrer)


@webadmin.route('/ethics/<int:project_id>/reviewers/remove/<int:reviewer_id>')
def remove_ethic_reviewer(project_id, reviewer_id):
    review = ProjectEthicReviewRecord.query.filter_by(reviewer_id=reviewer_id,
                                                      project_id=project_id).first()
    db.session.delete(review)
    db.session.commit()
    flash('Reviewer has been removed to the project review.', 'success')
    return redirect(request.referrer)


@webadmin.route('/ethics/<int:project_id>/reviewers/remove/all')
def remove_all_ethic_reviewers(project_id):
    project = ProjectRecord.query.get(project_id)
    for review in project.ethic_reviews:
        db.session.delete(review)
        db.session.commit()
    flash('All reviewers have been removed to the project review.', 'success')
    return redirect(request.referrer)


@webadmin.route('/submissions/<int:project_id>/ethics/<int:ethic_id>/reviews/send',
                methods=['GET', 'POST'])
def send_for_ethic_reviews(project_id, ethic_id):
    project = ProjectRecord.query.get(project_id)
    form = ProjectEthicReviewSendRecordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            for review in project.ethic_reviews:
                new_send = ProjectEthicReviewSendRecord()
                form.populate_obj(new_send)
                new_send.review_id = review.id
                new_send.to = review.reviewer.email
                new_send.sent_at = arrow.now(tz='Asia/Bangkok').datetime,
                db.session.add(new_send)
            db.session.commit()
            flash('The project has been sent for a review.')
            return redirect(url_for('webadmin.ethic_detail', project_id=project.id, ethic_id=ethic_id))
    return render_template('webadmin/send_reviews.html', form=form, project=project)


@webadmin.route('/submissions/<int:project_id>/ethics/<int:ethic_id>/reviews/sends', methods=['GET', 'POST'])
def view_send_ethic_records(project_id, ethic_id):
    project = ProjectRecord.query.get(project_id)
    ethic = ProjectEthicRecord.query.get(ethic_id)
    return render_template('webadmin/send_ethic_records.html', project=project, ethic=ethic)


@webadmin.route('/submissions/<int:project_id>/ethics/<int:ethic_id>/reviews/sends/<int:record_id>', methods=['GET', 'POST'])
def resend_for_ethic_review(project_id, record_id, ethic_id):
    project = ProjectRecord.query.get(project_id)
    send_record = ProjectEthicReviewSendRecord.query.get(record_id)
    form = ProjectEthicReviewSendRecordForm(obj=send_record)
    if request.method == 'POST':
        if form.validate_on_submit():
            new_send = ProjectEthicReviewSendRecord()
            form.populate_obj(new_send)
            new_send.to = send_record.to
            new_send.review_id = send_record.review.id
            new_send.sent_at = arrow.now(tz='Asia/Bangkok').datetime,
            db.session.add(new_send)
            db.session.commit()
            flash('The request has been resent.', 'success')
            return redirect(url_for('webadmin.view_send_ethic_records', project_id=project.id, ethic_id=ethic_id))
    return render_template('webadmin/send_reviews.html', project=project, form=form, to=send_record.to)


@webadmin.route('/submissions/<int:project_id>/ethics/<int:ethic_id>/reviews/<int:review_id>/add', methods=['GET', 'POST'])
def write_ethic_review(project_id, ethic_id, review_id):
    project = ProjectRecord.query.get(project_id)
    review = ProjectEthicReviewRecord.query.get(review_id)
    if review.submitted_at:
        return 'Thanks for reviewing.'
        '''
        return redirect(url_for('webadmin.confirm_review',
                                project_id=project.id, ethic_id=ethic.id))
        '''
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
def view_ethic_reviews(project_id, ethic_id):
    project = ProjectRecord.query.get(project_id)
    return render_template('webadmin/ethic_reviews.html', project=project, ethic_id=ethic_id)


@webadmin.route('/pubs/add', methods=['GET', 'POST'])
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
        else:
            flash(form.errors, 'danger')
        return redirect(url_for('webadmin.add_pub'))
    return render_template('webadmin/pub_add.html', form=form)


@webadmin.route('/journals/add', methods=['GET', 'POST'])
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
