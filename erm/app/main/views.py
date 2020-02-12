from flask import render_template
from . import main_bp as main
from app import db
from app.auth.forms import LoginForm


@main.route('/')
def index():
    form = LoginForm()
    return render_template('main/index.html', form=form)
