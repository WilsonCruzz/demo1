from flask import Blueprint, render_template, jsonify
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel

# url_prefix: The URL prefix that should be added to all URLs defined in the blueprint.
# url前綴
bp = Blueprint("auth", __name__, url_prefix="/auth")


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


@bp.route('/captcha/email')
def get_email_captcha():
    # /captcha/email?email=xxx
    email = request.args.get('email')
    source = string.digits * 6
    captcha = random.sample(source, 6)
    captcha = ''.join(captcha)
    msg = Message('test code', recipients=[email], body=f'code:{captcha}')
    mail.send(msg)
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({'code': 200, 'message': '', 'data': None})
