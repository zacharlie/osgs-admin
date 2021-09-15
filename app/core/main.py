# Main functions

from flask import Blueprint, render_template
from flask_login import login_required, current_user

main = Blueprint("main", __name__)

import logging

_LOG = logging.getLogger(__name__)


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


@main.route("/config")
@login_required
def page_config():
    from .models import Osgs

    osgs = Osgs.query.all()[0]

    import json

    osgs_repo = json.loads(osgs.config)["osgs_repo"]

    return render_template(
        "config.html",
        osgs=osgs,
        osgs_repo=osgs_repo,
    )
