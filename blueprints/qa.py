from flask import Blueprint, render_template

bp = Blueprint('qa', __name__, url_prefix='/')


# http://127.0.0.1:5000/
@bp.route('/')
def index():
    pass

@bp.route('/public_question')
def public_question():
    return render_template('base.html')

@bp.route('/search')
def search():
    return render_template('base.html')