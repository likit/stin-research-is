from app import create_app
from flask_admin.contrib.sqla import ModelView
from app import admin, db
from app.main.models import User


app = create_app()

admin.add_view(ModelView(User, db.session))

