from app.webadmin import webadmin_bp as webadmin
from flask import render_template, redirect, url_for
from app.project.models import ProjectRecord, ProjectReviewerGroup


@webadmin.route('/submissions')
def list_submissions():
    submissions = ProjectRecord.query.filter_by(status='submitted')
    return render_template('webadmin/submissions.html', submissions=submissions)


@webadmin.route('/submissions/<int:project_id>')
def submission_detail(project_id):
    project = ProjectRecord.query.get(project_id)
    return render_template('webadmin/submission_detail.html', project=project)


@webadmin.route('/submissions/<int:project_id>/reviewers/add')
def add_reviewers(project_id):
    project = ProjectRecord.query.get(project_id)
    groups = ProjectReviewerGroup.query.all()
    return render_template('webadmin/reviewers_add.html',
                           project=project,
                           groups=groups)
