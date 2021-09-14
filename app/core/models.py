from . import db
from flask_login import UserMixin

import os
from datetime import datetime

import logging

# from flask_sqlalchemy import func

from flask import render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash

_LOG = logging.getLogger(__name__)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.utcnow)


def init_db(database_path):
    _LOG.warning("Attempting to reinitialize database")

    if not os.path.exists(database_path):  # ensure existing db cannot be overwritten
        db.create_all()
        admin_user = User(
            username="admin",
            firstname="Administrator",
            lastname="",
            password=generate_password_hash("admin", method="sha256"),
        )
        db.session.add(admin_user)
        db.session.commit()

    else:
        return redirect(url_for("auth.page_login"))
    return render_template("bootstrap.html")
