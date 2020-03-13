from app.webadmin import webadmin_bp as webadmin
from flask import render_template, redirect, url_for
from app.project.models import ProjectRecord


@webadmin.route('/submissions')
def list_submissions():
    submissions = ProjectRecord.query.filter_by(status='submitted')
    return render_template('webadmin/submissions.html', submissions=submissions)
