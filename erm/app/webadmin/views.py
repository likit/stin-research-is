import arrow
from app.webadmin import webadmin_bp as webadmin
from wsgi import db
from flask import render_template, redirect, url_for, request, flash
from app.project.models import (ProjectRecord, ProjectReviewerGroup,
                                ProjectReviewSendRecord, ProjectReviewRecord,
                                )
from app.webadmin.forms import ProjectReviewSendRecordForm, ProjectReviewRecordForm
from app.project.forms import ProjectRecordForm


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
    if review.comment:
        return redirect(url_for('webadmin.confirm_review',
                                project_id=project.id, review_id=review.id))
    form = ProjectReviewRecordForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(review)
            review.submitted_at = arrow.now(tz='Asia/Bangkok').datetime
            db.session.add(review)
            db.session.commit()
            return redirect(url_for('webadmin.confirm_review', review_id=review.id, project_id=project.id))

    return render_template('webadmin/review_form.html', form=form, project=project, review=review)


@webadmin.route('/submissions/<int:project_id>/reviews/write/<int:review_id>/confirm', methods=['GET', 'POST'])
def confirm_review(project_id, review_id):
    project = ProjectRecord.query.get(project_id)
    review = ProjectReviewRecord.query.get(review_id)
    return render_template('webadmin/review_confirm.html', project=project, review=review)


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

