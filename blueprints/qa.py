from flask import Blueprint, render_template, request, g, redirect, url_for
from .forms import QuestionForm, AnswerForm
from models import QuestionModel, AnswerModel
from exts import db
from decorators import login_required

bp = Blueprint('qa', __name__, url_prefix='/')


@bp.route('/')
def index():
    questions = QuestionModel.query.order_by(QuestionModel.create_time.desc()).all()
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
            question = QuestionModel(title=title, content=content, author=g.user)
            db.session.add(question)
            db.session.commit()
            return redirect("/")
        else:
            print(form.errors)
            return redirect(url_for("qa.public_question"))

@bp.route("/qa/delete/<question_id>", methods=['POST'])
@login_required
def delete_qa(question_id):
    # /delete?question_id=1
    question = QuestionModel.query.get(question_id)
    if not question:
        return "No such question"

    # Delete all answers related to this question
    AnswerModel.query.filter_by(question_id=question_id).delete()

    db.session.delete(question)
    db.session.commit()
    return redirect(url_for("qa.index", question=question))


@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question = QuestionModel.query.get(qa_id)
    return render_template("detail.html", question=question)

# @bp.route("/answer/public", methods=['POST'])
@bp.post("/answer/public/")
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
        # If importing ID validation directly from the form fails, it won't be retrievable,
        # so use request.form.get("question.id") instead.
        return redirect(url_for("qa.qa_detail", qa_id=request.form.get("question_id")))

@bp.post("/answer/delete/<answer_id>")
@login_required
def delete_answer(answer_id):
    answer = AnswerModel.query.get(answer_id)
    if not answer:
        return "No such comment"
    db.session.delete(answer)
    db.session.commit()
    return redirect(url_for("qa.index"))


@bp.route("/search")
def search():
    # /search?q=flask
    # /search/<q>
    # post
    q = request.args.get("q")
    questions = QuestionModel.query.filter(QuestionModel.title.contains(q)).all()
    return render_template("index.html", questions=questions)