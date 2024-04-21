from flask import Blueprint, render_template
from exts import mail
from flask_mail import Message
# url_prefix: The URL prefix that should be added to all URLs defined in the blueprint.
# url前綴
bp = Blueprint("auth",__name__, url_prefix="/auth")

@bp.route('/login')
def login():
    pass

@bp.route('/register')
def register():
    return render_template('register.html')

@bp.route('/question')
def question():
    return render_template('base.html')

@bp.route('/search')
def search():
    return render_template('base.html')

@bp.route('/mail/test')
def mail_test():
    msg = Message('test subject', recipients=['200568068@student.georgianc.on.ca'], body='test body')
    mail.send(msg)
    return 'send mail success'