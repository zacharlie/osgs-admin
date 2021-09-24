from flask import Blueprint, render_template, redirect, url_for

main = Blueprint("main", __name__)


@main.route("/")
def page_index():
    return render_template("index.html")


@main.route("/about")
def page_about():
    return render_template("about.html")
