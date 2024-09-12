from flask import Blueprint, render_template
from flask_login import login_required


bp = Blueprint("Profile",__name__,url_prefix="/profile")

@bp.before_request
@login_required
def handle_route_permissions():
    # enforce login on all views
    pass

@bp.route("/")
def index():
    return render_template('profile/index.html')
