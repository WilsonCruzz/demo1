from flask import Blueprint, render_template, jsonify, redirect, url_for
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel
from .forms import RegisterForm
from models import UserModel
from werkzeug.security import generate_password_hash

# url_prefix: The URL prefix that should be added to all URLs defined in the blueprint.
# url前綴
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route('/login')
def login():
    return "login"


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # 驗證用戶提交的郵箱和驗證碼是否正確
        form = RegisterForm(request.form)
        if form.validate():
            email = form.email.data
            username = form.username.data
            password = form.password.data
            user = UserModel(email=email, username=username, password=generate_password_hash(password))
            db.session.add(user)
            db.session.commit()
            return redirect(url_for("auth.login"))
        else:
            print(form.errors)
            return redirect(url_for("auth.register"))



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
    # I/O: input/output
    msg = Message('test code', recipients=[email], body=f'code:{captcha}')
    mail.send(msg)
    email_captcha = EmailCaptchaModel(email=email, captcha=captcha)
    db.session.add(email_captcha)
    db.session.commit()
    return jsonify({'code': 200, 'message': '', 'data': None})
