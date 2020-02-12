from flask import Blueprint

researcher_bp = Blueprint('researcher', __name__)

from . import views