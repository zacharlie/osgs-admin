from flask import Blueprint, g, render_template, flash
from flask_login import login_required
from pathlib import Path

ops = Blueprint("ops", __name__)

from .models import Osgs

from .utils import hello_world, hello_sleepy_world

##################################################
# Example Pages for dev purposes #


@ops.route("/examples/reactive")
def page_eg_reactive():
    return render_template("ops/reactive.html")


##################################################
# # Example pages end #
##################################################


@ops.route("/ops/clone")
@login_required
def page_clone():
    osgs = Osgs.query.all()[0]
    hw = hello_world()
    from .utils.example import flash_example_message, return_example_message

    flash_example_message()
    eg = return_example_message()
    return render_template("ops/clone.html", osgs=osgs, hw=hw, eg=eg)


@ops.route("/ops/clone", methods=["POST"])
@login_required
def form_clone_post():
    osgs = Osgs.query.all()[0]
    hw = hello_world()
    flash(hello_sleepy_world())  # g.operation_req_active=False
    return render_template("ops/clone.html", osgs=osgs, hw=hw)


@ops.app_context_processor
def set_operation_req():
    return dict(request_active=False)


"""

# Before First Request To Public BP
from threading import Lock
public._before_request_lock = Lock()
public._got_first_request = False

def init_public_bp():
    if public._got_first_request:
        return  # or pass
    with public._before_request_lock:
        public._got_first_request = True
        print('THIS IS THE FIRST REQUEST!')
        # Do more stuff here...
public.before_request(init_public_bp)


"""


"""
@ops.app_context_processor
def set_operation_req():
    g.operation_req_active = False
    return dict(request_active=g.request_active)
"""


"""
@ops.context_processor
def set_operation_req():
    g.operation_req_active = False
    return dict(request_active=g.request_active)

"""
"""
@ops.before_request
def before_req():
    g.operation_req_active = True
    return dict(request_active=g.request_active)
"""

"""
configure-ssl-self-signed - Create a self signed cert for local testing
configure            - Configure the initial stack including nginx, scp and hugo-watcher
deploy-qgis-desktop  - Run QGIS Desktop in your web browser
deploy               - Deploy the initial stack including nginx, scp and hugo-watcher
disable-all-services - Disable all services - does not actually stop them
docs                 - Generate documentation and place results in docs folder.
prepare-templates    - Prepare templates
ps                   - List all running docker contains
"""