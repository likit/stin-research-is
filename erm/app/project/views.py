from flask import render_template

from app import db
from . import project_bp as project
from .models import *


@project.route('/')
def list_projects():
    projects = ProjectRecord.query.order_by(ProjectRecord.created_at)
    return render_template('project/index.html', projects=projects)


@project.route('/detail/<int:project_id>')
def display_project(project_id):
    project = ProjectRecord.query.get(project_id)
    return render_template('project/detail.html', project=project)

