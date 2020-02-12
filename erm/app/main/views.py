from . import main_bp as main
from app import db


@main.route('/')
def index():
    return '<h1>Welcome to the lightest RMS ever.</h1>'
