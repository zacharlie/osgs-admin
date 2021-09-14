from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint("auth", __name__)


@auth.route("/login")
def page_login():
    return render_template("login.html")


@auth.route("/login", methods=["POST"])
def form_login_post():
    username = request.form.get("username")
    password = request.form.get("password")
    remember = True if request.form.get("remember") else False

    user = User.query.filter_by(username=username).first()

    # check if user actually exists
    # take the user supplied password, hash it, and compare it to the hashed password in database
    if not user or not check_password_hash(user.password, password):
        flash("Invalid credentials.")
        return redirect(
            url_for("auth.page_login")
        )  # if user doesn't exist or password is wrong, reload the page

    # if the above check passes, then we know the user has the right credentials
    login_user(user, remember=remember)
    return redirect(url_for("main.page_dashboard"))


@auth.route("/newuser")
@login_required
def page_newuser():
    return render_template("newuser.html")


@auth.route("/newuser", methods=["POST"])
@login_required
def form_newuser_post():

    username = request.form.get("username")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    password = request.form.get("password")

    user = User.query.filter_by(
        username=username
    ).first()  # if value returned, username already exists

    if (
        user
    ):  # if a user is found, we want to redirect back to newuser page so user can try again
        flash("Username already exists")
        return redirect(url_for("auth.page_newuser"))

    # create new user with the form data. Hash the password so plaintext version isn't saved.
    new_user = User(
        username=username,
        firstname=firstname,
        lastname=lastname,
        password=generate_password_hash(password, method="sha256"),
    )

    # add the new user to the database
    db.session.add(new_user)
    db.session.commit()

    return redirect(url_for("auth.page_login"))


@auth.route("/logout")
@login_required
def page_logout():
    logout_user()
    return redirect(url_for("main.page_index"))
