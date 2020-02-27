import arrow
from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required

from app import db
from . import project_bp as project
from .models import *
from .forms import ProjectRecordForm, ApplicationForm
from app.main.models import User



@project.route('/')
def list_projects():
    projects = ProjectRecord.query.all()
    return render_template('project/index.html', projects=projects)


@project.route('/user/<int:user_id>')
@login_required
def list_created_projects(user_id):
    user = User.query.get(user_id)
    projects = user.projects
    return render_template('project/created_projects.html', projects=projects)


@project.route('/detail/<int:project_id>')
def display_project(project_id):
    project = ProjectRecord.query.get(project_id)
    return render_template('project/detail.html', project=project)


@project.route('/edit/<int:project_id>', methods=['GET', 'POST'])
@login_required
def edit_project(project_id):
    project = ProjectRecord.query.get(project_id)
    form = ProjectRecordForm(obj=project)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(project)
            project.updated_at = arrow.now(tz='Asia/Bangkok').datetime
            db.session.add(project)
            db.session.commit()
            flash('Data have been updated.', 'success')
        else:
            flash('Error occurred.', 'danger')
        return redirect(url_for('project.display_project', project_id=project.id))
    return render_template('project/project_edit.html', form=form)


@project.route('/<int:project_id>/application/new', methods=['GET', 'POST'])
@login_required
def add_application(project_id):
    project = ProjectRecord.query.get(project_id)
    form = ApplicationForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            new_app = Application()
            form.populate_obj(new_app)
            new_app.project = project
            db.session.add(new_app)
            db.session.commit()
            flash('Application has been recorded.', 'success')
        else:
            flash('Error occurred.', 'danger')
        return redirect(url_for('project.display_project', project_id=project.id))
    return render_template('project/application_add.html', form=form)


@project.route('/application/<int:app_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_application(app_id):
    app = Application.query.get(app_id)
    form = ApplicationForm(obj=app)
    if request.method == 'POST':
        if form.validate_on_submit():
            form.populate_obj(app)
            db.session.add(app)
            db.session.commit()
            flash('Application has been updated.', 'success')
        else:
            flash('Error occurred.', 'danger')
        return redirect(url_for('project.display_project', project_id=app.project.id))
    return render_template('project/application_add.html', form=form)


@project.route('/application/<int:app_id>/remove', methods=['GET', 'POST'])
@login_required
def remove_application(app_id):
    application = Application.query.get(app_id)
    project_id = application.project_id
    try:
        db.session.delete(application)
        db.session.commit()
    except:
        flash('Error occurred.', 'danger')
    else:
        flash('Application has been removed.', 'success')
    return redirect(url_for('project.display_project', project_id=project_id))
