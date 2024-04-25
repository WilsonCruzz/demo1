from functools import wraps
from flask import g, redirect, url_for
def login_required(func):
    # remain function name and info (closure)
    @wraps(func)
    def inner(*args, **kwargs):
        if g.user:
            return func(*args, **kwargs)
        else:
            return redirect(url_for("auth.login"))
    return inner
