import os
from flask_mail import Mail
from flask import Flask, flash, redirect
from flask_migrate import Migrate
from flask_admin import Admin
from flask_login import LoginManager, current_user
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv
from functools import wraps

load_dotenv()

admin = Admin()
db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()
mail = Mail()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL')

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')
    app.config['MAIL_SERVER'] = 'smtp.gmail.com'
    app.config['MAIL_PORT'] = 587
    app.config['MAIL_USE_TLS'] = True
    app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
    app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD')
    app.config['MAIL_DEFAULT_SENDER'] = ('STIN-RESEARCH-CENTER', os.environ.get('MAIL_USERNAME'))

    mail.init_app(app)

    from app.main import main_bp as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from app.auth import auth_bp as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    from app.researcher import researcher_bp as researcher_blueprint
    app.register_blueprint(researcher_blueprint, url_prefix='/researcher')

    from app.project import project_bp as project_blueprint
    app.register_blueprint(project_blueprint, url_prefix='/project')

    from app.webadmin import webadmin_bp as webadmin_blueprint
    app.register_blueprint(webadmin_blueprint, url_prefix='/webadmin')

    admin.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'

    return app


def superuser(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 1:
            flash('You do not have permission to view access this page.', 'warning')
            return redirect('/')
        return f(*args, **kwargs)
    return decorated_function
