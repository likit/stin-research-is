from flask import render_template
from flask_login import login_required
from app.main.models import User
from app.researcher.models import Profile
from app import db
from . import researcher_bp as researcher


@researcher.route('/profile/<int:user_id>')
@login_required
def show_profile(user_id):
    user = User.query.get(user_id)
    if not user.profile:
        profile = Profile(user_id=user.id)
        db.session.add(profile)
        db.session.commit()
    return render_template('researcher/profile.html', user=user)