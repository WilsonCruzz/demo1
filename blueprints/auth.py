from flask import Blueprint

# url_prefix: The URL prefix that should be added to all URLs defined in the blueprint.
# url前綴
bp = Blueprint("auth",__name__, url_prefix="/auth")

@bp.route('/login')
def login():
    return 'login page'