from flask import Blueprint, render_template, request, g, redirect, url_for
from .forms import QuestionForm
from models import QusetionModel
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

@bp.route('/search')
def search():
    return render_template('base.html')

@bp.route("/qa/detail/<qa_id>")
def qa_detail(qa_id):
    question = QusetionModel.query.get(qa_id)
    return render_template("detail.html", question=question)