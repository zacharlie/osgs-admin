from . import db
from flask_login import UserMixin

import os
from datetime import datetime

import logging

# from flask_sqlalchemy import func

from flask import render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash
from base64 import b64encode

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
        # credential = b64encode(os.urandom(43)).decode("utf-8")[4:37]  # set random (production mode)
        credential = "admin"  # admin admin (development mode)
        db.create_all()
        admin_user = User(
            username="admin",
            firstname="Administrator",
            lastname="",
            password=generate_password_hash(credential, method="sha256"),
        )
        db.session.add(admin_user)
        db.session.commit()
        set_config_defaults()
        return render_template("bootstrap.html", credential=credential)
    else:
        _LOG.warning("An attempt to create the existing database was made")
        flash("Database already exists")
        return redirect(url_for("auth.page_login"))


class Osgs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)

    def __init__(self, **kwargs):
        db.create_all()
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.created = kwargs.get("created")
        db.session.commit()


def set_config_defaults():
    config_defaults = Osgs(name="Open Source GIS Stack")
    db.session.add(config_defaults)
    db.session.commit()
