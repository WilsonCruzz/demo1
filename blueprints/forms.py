import wtforms
from wtforms.validators import Email, Length, EqualTo, InputRequired
from models import UserModel, EmailCaptchaModel
from exts import db

# 驗證前端提交的數據是否符合要求
class RegisterForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='Please input correct email address')])
    captcha = wtforms.StringField(validators=[Length(min=6, max=6, message='Please input correct captcha')])
    username = wtforms.StringField(validators=[Length(min=3, max=20, message='Please input correct username')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='Please input correct password')])
    password_confirm = wtforms.StringField(validators=[EqualTo('password', message='Password is not same')])


#   check if email has been registered
    def validate_email(self, field):
        email = field.data
        user = UserModel.query.filter_by(email=email).first()
        if user:
            raise wtforms.ValidationError('Email has been registered')

    def validate_captcha(self, field):
        captcha = field.data
        email = self.email.data
        captcha_model = EmailCaptchaModel.query.filter_by(email=email, captcha=captcha).first()
        if not captcha_model:
            raise wtforms.ValidationError('Captcha is not correct')
        else:
            db.session.delete(captcha_model)
            db.session.commit()


class LoginForm(wtforms.Form):
    email = wtforms.StringField(validators=[Email(message='Please input correct email address')])
    password = wtforms.StringField(validators=[Length(min=6, max=20, message='Please input correct password')])


class QuestionForm(wtforms.Form):
    title = wtforms.StringField(validators=[Length(min=3,max=100,message="title error")])
    content = wtforms.StringField(validators=[Length(min=3,message="content error")])


class AnswerForm(wtforms.Form):
    content = wtforms.StringField(validators=[Length(min=1, message="content error")])
    question_id = wtforms.IntegerField(validators=[InputRequired(message="must input question id")])