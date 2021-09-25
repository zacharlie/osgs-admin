from . import db
from flask import current_app
from flask_login import UserMixin

import os
from datetime import datetime

# from flask_sqlalchemy import func

from flask import render_template, flash, redirect, url_for
from werkzeug.security import generate_password_hash

import json


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    password = db.Column(db.String(100))
    firstname = db.Column(db.String(255))
    lastname = db.Column(db.String(255))
    created = db.Column(db.DateTime, default=datetime.utcnow)


def init_db(database_path):
    current_app.logger.warning("Attempting to reinitialize database")

    if not os.path.exists(database_path):  # ensure existing db cannot be overwritten
        from .utils.sec import key_gen

        if os.environ.get("FLASK_ENV") == "development":
            credential = "admin"  # admin admin (development mode)
        else:
            credential = key_gen(18)  # set random (production mode)
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
        current_app.logger.warning(
            "An attempt to create the existing database was made"
        )
        flash("Database already exists")
        return redirect(url_for("auth.page_login"))


class Osgs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True)
    created = db.Column(db.DateTime, default=datetime.utcnow)
    fqdn = db.Column(db.String(255))
    root = db.Column(db.String(255))
    # Store generic config as json object to allow dynamic values as
    # needed, whilst keeping data consolidated in the sqlite db for
    # simplifying migration and deployment, whilst remaining distinct
    # from the application config.
    config = db.Column(db.JSON())

    def __init__(self, **kwargs):
        db.create_all()
        self.id = kwargs.get("id")
        self.name = kwargs.get("name")
        self.created = kwargs.get("created")
        self.fqdn = kwargs.get("fqdn")
        self.root = kwargs.get("root")
        self.config = kwargs.get("config")
        db.session.commit()


def set_config_defaults():

    from .config import osgs_default_config

    config_defaults = Osgs(
        name="Open Source GIS Stack",
        fqdn="www.example.com",
        root=os.path.join(os.path.realpath(os.path.dirname(__file__)), "osgs"),
        config=json.dumps(osgs_default_config),
    )
    db.session.add(config_defaults)
    db.session.commit()
