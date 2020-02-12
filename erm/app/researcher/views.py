from flask import render_template
from flask_login import login_required
from . import researcher_bp as researcher


@researcher.route('/profile')
@login_required
def show_profile():
    return render_template('researcher/profile.html')