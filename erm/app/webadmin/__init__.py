from flask import Blueprint

webadmin_bp = Blueprint('webadmin', __name__)

from . import views
