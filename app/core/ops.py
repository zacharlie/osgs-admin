# Operations functions

from flask import Blueprint, render_template
from flask_login import login_required

ops = Blueprint("ops", __name__)

import logging

_LOG = logging.getLogger(__name__)

from .models import Osgs

from .utils import hello_world


@ops.route("/ops/clone")
@login_required
def page_index():
    osgs = Osgs.query.all()[0]
    hw = hello_world()
    return render_template("ops/clone.html", osgs=osgs, hw=hw)
