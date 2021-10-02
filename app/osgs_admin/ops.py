from flask import Blueprint, g, render_template, flash, jsonify, redirect
from flask_login import login_required

ops = Blueprint("ops", __name__)

from .models import Osgs
import json


@ops.route("/config")
@login_required
def page_config():
    osgs = Osgs.query.all()[0]
    osgs_config = json.loads(osgs.config)

    return render_template(
        "config/index.html",
        osgs=osgs,
        osgs_config=osgs_config,
    )


@ops.route("/config/system")
@ops.route("/config/system/config")
@ops.route("/config/config")
@login_required
def redirect_config_system_config():
    return redirect("/config?section=config", 301)


@ops.route("/config/system/env")
@ops.route("/config/env")
@login_required
def redirect_config_system_env():
    return redirect("/config?section=config", 301)


@ops.route("/config/system/compose")
@ops.route("/config/compose")
@login_required
def redirect_config_system_compose():
    return redirect("/config?section=compose", 301)


@ops.route("/config/setup")
@login_required
def page_config_setup():
    osgs = Osgs.query.all()[0]
    osgs_config = json.loads(osgs.config)

    return render_template(
        "config/setup.html",
        osgs=osgs,
        osgs_config=osgs_config,
    )


@ops.route("/config/setup/routes")
@login_required
def redirect_config_setup_routes():
    return redirect("/config/setup?section=routes", 301)


@ops.route("/config/setup/repo")
@login_required
def redirect_config_setup_repo():
    return redirect("/config/setup?section=repo", 301)


@ops.route("/config/setup/ops")
@login_required
def redirect_config_setup_ops():
    return redirect("/config/setup?section=ops", 301)


@ops.route("/config/services")
@login_required
def page_config_services():
    osgs = Osgs.query.all()[0]
    osgs_config = json.loads(osgs.config)

    return render_template(
        "config/services.html",
        osgs=osgs,
        osgs_config=osgs_config,
    )


@ops.route("/config/apis")
@login_required
def page_config_apis():
    osgs = Osgs.query.all()[0]
    osgs_config = json.loads(osgs.config)

    return render_template(
        "config/apis.html",
        osgs=osgs,
        osgs_config=osgs_config,
    )


@ops.route("/config/backup")
@login_required
def page_config_backup():
    osgs = Osgs.query.all()[0]
    osgs_config = json.loads(osgs.config)

    return render_template(
        "config/backup.html",
        osgs=osgs,
        osgs_config=osgs_config,
    )


@ops.route("/config/backup/export")
@login_required
def redirect_config_backup_export():
    return redirect("/config/backup?section=export", 301)


@ops.route("/config/reset")
@login_required
def page_config_reset():
    osgs = Osgs.query.all()[0]
    osgs_config = json.loads(osgs.config)

    return render_template(
        "config/reset.html",
        osgs=osgs,
        osgs_config=osgs_config,
    )


@ops.route("/config/security")
@login_required
def page_config_security():
    osgs = Osgs.query.all()[0]
    osgs_config = json.loads(osgs.config)

    return render_template(
        "config/security.html",
        osgs=osgs,
        osgs_config=osgs_config,
    )


@ops.route("/config/security/ssl")
@login_required
def redirect_config_security_ssl():
    return redirect("/config/security?section=ssl", 301)


@ops.route("/config/security/ssh")
@login_required
def redirect_config_security_ssh():
    return redirect("/config/security?section=ssh", 301)


@ops.route("/config/security/oauth")
@login_required
def redirect_config_security_oauth():
    return redirect("/config/security?section=oauth", 301)


@ops.route("/system/resources/usage", methods=["GET"])
def rest_system_resource_usage():
    from .utils.sysutils import get_sys_stats

    system_stats = get_sys_stats()
    return jsonify(system_stats)


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
