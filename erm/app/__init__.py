import os
from flask import Flask
from flask_migrate import Migrate
from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy
from dotenv import load_dotenv

load_dotenv()

admin = Admin()
db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres+psycopg2://postgres@{}:{}/{}'.format(
        os.environ.get('DATABASE_HOST'),
        os.environ.get('DATABASE_PORT', 5432),
        os.environ.get('DATABASE'),
    )

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

    from app.main import main_bp as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/')

    from app.auth import auth_bp as auth_blueprint
    app.register_blueprint(auth_blueprint, url_prefix='/auth')

    admin.init_app(app)
    db.init_app(app)
    migrate.init_app(app, db)
    return app
