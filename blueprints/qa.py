from flask import Blueprint, render_template, request, g, redirect, url_for
from .forms import QuestionForm, AnswerForm
from models import QusetionModel, AnswerModel
from exts import db
from decorators import login_required



bp = Blueprint('qa', __name__, url_prefix='/')


# http://127.0.0.1:5000/
@bp.route('/')
def index():
    questions = QusetionModel.query.order_by(QusetionModel.create_time.desc()).all()
    return render_template("index.html", questions=questions)


@bp.route("/qa/public", methods=['GET', 'POST'])
@login_required
def public_qa():
    if request.method == 'GET':
        return render_template("public_question.html")
    else:
        form = QuestionForm(request.form)
        if form.validate():
            title = form.title.data
            content = form.content.data
            question = QusetionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))


# @bp.route('/public_question')
# def public_question():
#     return render_template('base.html')


@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question = QusetionModel.query.get(qa_id)
    return render_template("detail.html", question=question)

# @bp.route("/answer/public", methods=['POST'])
@bp.post("/answer/public")
@login_required
def public_answer():
    form = AnswerForm(request.form)
    if form.validate():
        content = form.content.data
        question_id = form.question_id.data
        answer = AnswerModel(content=content, question_id=question_id, author_id=g.user.id)
        db.session.add(answer)
        db.session.commit()
        return redirect(url_for("qa.qa_detail", qa_id=question_id))
    else:
        print(form.errors)
        # 如果直接從form導入id驗證失敗的狀況下會取不到，所以使用request.form.get("question.id")
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question.id")))


@bp.route("/search")
def search():
    # /search?q=flask
    # /search/<q>
    # post
    q = request.args.get("q")
    questions = QusetionModel.query.filter(QusetionModel.title.contains(q)).all()
    return render_template("index.html", questions=questions)

# url傳參
# 郵件發送
# ajax
# orm與數據庫
# Jinja2模板
# cookie和session原理
# 搜索

#