from flask_login import current_user
from flask import redirect, url_for
from functools import wraps

def logout_required(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        if current_user.is_authenticated:
            return redirect(url_for('Home.index'))
        else:
            return func(*args,**kwargs)
    return wrapper