from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required
from .models import User
from . import db

auth = Blueprint("auth", __name__)

import logging

_LOG = logging.getLogger(__name__)


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


@auth.route("/users")
@login_required
def page_users():

    sort = request.args.get("sort", "id", type=str)
    sort = sort if sort in ["id", "name", "user", "first", "last"] else "id"
    sortmap = {
        "id": "id",
        "name": "username",
        "user": "username",
        "first": "firstname",
        "last": "lastname",
    }
    sort = sortmap[sort]

    order = request.args.get("order", "asc", type=str)
    order = order if order in ["asc", "desc"] else "asc"

    page = request.args.get("page", 1, type=int)

    if order == "desc":
        query = User.query.order_by(getattr(User, sort).desc())
    else:
        query = User.query.order_by(getattr(User, sort).asc())

    USERS_PER_PAGE = 10
    userlist = query.paginate(page, USERS_PER_PAGE, True)

    return render_template(
        "users.html", userlist=userlist, sort=sort, order=order, page=page
    )


@auth.route("/users/create")
@login_required
def page_user_create():
    return render_template("users/create.html")


@auth.route("/users/create", methods=["POST"])
@login_required
def form_user_create_post():

    username = request.form.get("username")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")
    password = request.form.get("password")

    user = User.query.filter_by(
        username=username
    ).first()  # if value returned, username already exists

    if (
        user
    ):  # if a user is found, we want to redirect back to user creation page so user can try again
        flash("Username already exists")
        return redirect(url_for("auth.page_user_create"))

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

    flash(f"User {username} created")

    return redirect(url_for("auth.page_users"))


@auth.route("/users/delete/<userid>")
@login_required
def page_delete_user(userid):
    user = User.query.filter_by(id=userid).first()
    if not user:
        flash("User does not exist")
        redirect(url_for("auth.page_users"))
    return render_template("users/delete.html", user=user)


@auth.route("/users/delete/<userid>", methods=["POST"])
@login_required
def form_user_delete_post(userid):
    user = User.query.filter_by(id=userid).first()
    if user:
        deleted_user = user.username
        db.session.delete(user)
        db.session.commit()
        flash(f"User {deleted_user} has been removed")
    else:
        flash(f"User does not exist")

    return redirect(url_for("auth.page_users"))


@auth.route("/users/edit/<userid>")
@login_required
def page_edit_user(userid):
    user = User.query.filter_by(id=userid).first()
    if not user:
        flash("User does not exist")
        redirect(url_for("auth.page_users"))
    return render_template("users/edit.html", user=user)


@auth.route("/users/edit/<userid>", methods=["POST"])
@login_required
def form_user_edit_post(userid):

    # username = request.form.get("username")
    firstname = request.form.get("firstname")
    lastname = request.form.get("lastname")

    user = User.query.filter_by(id=userid).first()

    if not user:
        flash("User does not exist")
        redirect(url_for("auth.page_users"))

    # update user information
    # user.username = username
    user.firstname = firstname
    user.lastname = lastname
    db.session.commit()

    flash(f"Information updated for {user.username}")
    return redirect(url_for("auth.page_users"))


@auth.route("/users/reset/<userid>")
@login_required
def page_reset_user(userid):
    user = User.query.filter_by(id=userid).first()
    if not user:
        flash("User does not exist")
        redirect(url_for("auth.page_users"))
    return render_template("users/reset.html", user=user)


@auth.route("/users/reset/<userid>", methods=["POST"])
@login_required
def form_user_reset_post(userid):
    password = request.form.get("password")
    user = User.query.filter_by(id=userid).first()
    if not user:
        flash("User does not exist")
        redirect(url_for("auth.page_users"))
    user.password = generate_password_hash(password, method="sha256")
    db.session.commit()
    flash(f"Password updated for {user.username}")
    return redirect(url_for("auth.page_users"))


@auth.route("/logout")
@login_required
def page_logout():
    logout_user()
    return redirect(url_for("main.page_index"))
