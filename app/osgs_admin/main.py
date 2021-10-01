from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint("main", __name__)


@main.route("/")
def page_index():
    return render_template("index.html")


@main.route("/about")
def page_about():
    return render_template("about.html")


@main.route("/dashboard")
@login_required
def page_dashboard():
    return render_template(
        "dashboard/index.html",
        firstname=current_user.firstname,
        lastname=current_user.lastname,
    )


@main.route("/dashboard/docker")
@login_required
def page_dashboard_docker():
    return render_template(
        "dashboard/docker.html",
        firstname=current_user.firstname,
        lastname=current_user.lastname,
    )


@main.route("/dashboard/osgs")
@login_required
def page_dashboard_osgs():
    return render_template(
        "dashboard/osgs.html",
        firstname=current_user.firstname,
        lastname=current_user.lastname,
    )
