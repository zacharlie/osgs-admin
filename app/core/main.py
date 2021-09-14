from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint("main", __name__)


@main.route("/")
def page_index():
    return render_template("index.html")


@main.route("/dashboard")
@login_required
def page_dashboard():
    return render_template(
        "dashboard.html",
        firstname=current_user.firstname,
        lastname=current_user.lastname,
    )
