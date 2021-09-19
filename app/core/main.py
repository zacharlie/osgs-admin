from flask import Blueprint, render_template, redirect, url_for

main = Blueprint("main", __name__)


@main.route("/")
def page_index():
    return render_template("index.html")


@main.route("/about")
def page_about():
    return render_template("about.html")


@main.route("/task/example", methods=["get"])
def page_task_example():
    result = None
    return render_template("ops/setup.html", result=result)


@main.route("/task/example", methods=["POST"])
def form_task_example_post():
    from .tasks import test

    result = test.result
    return render_template("ops/setup.html", result=result)
