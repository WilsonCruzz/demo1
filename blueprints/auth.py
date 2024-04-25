from flask import Blueprint, render_template, jsonify, redirect, url_for, session
from exts import mail, db
from flask_mail import Message
from flask import request
import string
import random
from models import EmailCaptchaModel, UserModel
from .forms import RegisterForm, LoginForm
from werkzeug.security import generate_password_hash, check_password_hash



# url_prefix: The URL prefix that should be added to all URLs defined in the blueprint.
# url前綴
bp = Blueprint("auth", __name__, url_prefix="/auth")


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        form = LoginForm(request.form)
        if form.validate():
            email = form.email.data
            password = form.password.data
            user = UserModel.query.filter_by(email=email).first()
            if not user:
                print('user is not exist')
                return redirect(url_for("auth.login"))
            # 使用函數去判斷加密後密碼和原生密碼是否匹配
            if check_password_hash(user.password, password):
                # cookie 不是何儲存太多數據 一般用來存放登錄授權
                # flask的session經過加密後存在cookie中
                # 用session把資訊存在cookie中
                session['user_id'] = user.id
                return redirect("/")
            else:
                print('password error')
                return redirect(url_for("auth.login"))
        else:
            return redirect(url_for("auth.login"))



@bp.route("/logout")
def logout():
    session.clear()
    return redirect("/")


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        # validate email, username, password
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

@bp.route('/profile')
def profile():
    user_id = session.get('user_id')
    user = UserModel.query.get(user_id)
    return render_template('profile.html', user=user)