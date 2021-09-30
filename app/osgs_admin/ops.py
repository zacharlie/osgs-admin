from flask import Blueprint, g, render_template, flash, jsonify
from flask_login import login_required

ops = Blueprint("ops", __name__)

from .models import Osgs


@ops.route("/config")
@login_required
def page_config():

    osgs = Osgs.query.all()[0]

    import json

    osgs_repo = json.loads(osgs.config)["osgs_repo"]

    return render_template(
        "config/index.html",
        osgs=osgs,
        osgs_repo=osgs_repo,
    )


##################################################
# Example Pages for dev purposes #

from .utils import hello_world, hello_sleepy_world


@ops.route("/examples/reactive")
def page_eg_reactive():
    return render_template("ops/reactive.html")


@ops.route("/task/example", methods=["get"])
def page_task_example():
    result = None
    return render_template("ops/setup.html", result=result)


@ops.route("/task/example", methods=["POST"])
def form_task_example_post():
    from .tasks.utils import long_task

    task = long_task.apply_async()

    if task:
        result = {
            "id": task.id,
        }
    else:
        result = None

    return render_template("ops/setup.html", result=result)


@ops.route("/task/progress/<task_id>", methods=["GET"])
def page_task_progress(task_id):
    return render_template("ops/progress.html", task_id=task_id)


@ops.route("/task/status/<task_id>", methods=["GET"])
def rest_task_status(task_id):
    from celery.result import AsyncResult
    from .tasks import celery

    # task = long_task.AsyncResult(task_id)
    task = AsyncResult(task_id, app=celery)
    if task.state == "PENDING":
        # job did not start yet
        response = {
            "state": task.state,
            "current": 0,
            "total": 1,
            "status": "Pending...",
        }
    elif task.state != "FAILURE":
        response = {
            "state": task.state,
            "current": task.info.get("current", 0),
            "total": task.info.get("total", 1),
            "status": task.info.get("status", ""),
        }
        if "result" in task.info:
            response["result"] = task.info["result"]
    else:
        # something went wrong in the background job
        response = {
            "state": task.state,
            "current": 1,
            "total": 1,
            "status": str(task.info),  # this is the exception raised
        }
    return jsonify(response)


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
