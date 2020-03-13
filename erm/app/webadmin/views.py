from app.webadmin import webadmin_bp as webadmin


@webadmin.route('/submissions')
def list_submissions():
    return 'here you go.'
