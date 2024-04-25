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
            # use function check_password_hash to check password
            if check_password_hash(user.password, password):
                # Cookies are not for storing too much data, they are generally used to store login authorization
                # Flask's session is encrypted and stored in cookies
                # Use session to store information in cookies
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
    existing_user = UserModel.query.filter_by(email=email).first()
    if existing_user:
        return jsonify({'code': 400, 'message': 'email is exist', 'data': None})

    # Check if a captcha already exists for this email
    existing_captcha = EmailCaptchaModel.query.filter_by(email=email).first()
    if existing_captcha:
        # Delete the existing captcha
        db.session.delete(existing_captcha)
        db.session.commit()

    source = string.digits * 6
    captcha = random.sample(source, 6)
    captcha = ''.join(captcha)
    # I/O: input/output
    msg = Message('[Verification Code] Welcome to the Georgian College Forum!', recipients=[email], body =f'''Dear User,

Thank you for registering with the Georgian College Forum! Your verification code is: {captcha}.

Please use this code to complete the registration process. We look forward to you sharing your ideas, engaging in discussions, and connecting with others on the forum.

Wishing you a pleasant experience on the Georgian College Forum!

Thank you,
Georgian College Forum Team''')
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