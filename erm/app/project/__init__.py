from flask import Blueprint

project_bp = Blueprint('project', __name__)

from . import views