from flask import render_template
from flask_mail import Message
from . import main_bp as main
from app import db, mail
from app.auth.forms import LoginForm


@main.route('/')
def index():
    form = LoginForm()
    return render_template('main/index.html', form=form)


@main.route('/send-mail')
def send_mail():
    message = Message("Test sending email from Flask",
                      recipients=['likit.pre@mahidol.edu'])
    message.body = 'New email from the Flask system has arrived.'
    try:
        mail.send(message)
    except:
        return 'Mail failed to send.'
    return 'Mail sent.'