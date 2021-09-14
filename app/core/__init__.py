from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from base64 import b64encode
import os

import logging

_LOG = logging.getLogger(__name__)

db = SQLAlchemy()


def initialize():
    app = Flask(__name__)

    # app.config["SECRET_KEY"] = "fzHofj7khjMslfoTVU5OONxqkcmCYPxBE5BygBaW9zyqT"
    app.config["SECRET_KEY"] = b64encode(os.urandom(43)).decode("utf-8")[4:37]
    app.config["DATABASE_FILE"] = "db.sqlite"
    # db path uses sqlite:/// for relative and sqlite://// for absolute
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + app.config["DATABASE_FILE"]
    app.config["SQLALCHEMY_ECHO"] = True

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.page_login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        # since the user_id is just the primary key of our user table, use it in the query for the user
        return User.query.get(int(user_id))

    # blueprint for auth routes in our app
    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    # blueprint for non-auth parts of app
    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    return app


app = initialize()

# db
app.app_dir = os.path.realpath(os.path.dirname(__file__))
app.database_path = os.path.join(app.app_dir, app.config["DATABASE_FILE"])
database_path = app.database_path


def check_db(database_path):
    db_exists = True if os.path.exists(database_path) else False
    return db_exists


# This is just for frontend and should be disabled to force a 405 when requested without posting
@app.route("/bootstrap", methods=["GET"])
def page_bootstrap_dev():
    return render_template("bootstrap.html")


# Bootstap process for initiating new database
@app.route("/bootstrap", methods=["POST"])
def page_bootstrap():
    from .models import init_db as initialize_database

    initialize_database(app.database_path)
    return render_template("bootstrap.html")


# Context processors


@app.context_processor
def database_state():
    def check_database_state():
        return check_db(app.database_path)

    return dict(check_database_state=check_database_state)


@app.context_processor
def get_site_title():
    g.site_title = "OSGS Admin"
    return dict(site_logo=g.site_title)


@app.context_processor
def get_site_logo():
    g.site_logo = "/static/osgs.svg"
    return dict(site_logo=g.site_logo)


# Error codes

for i in [404, 405]:

    @app.errorhandler(i)
    def error(error):
        return render_template("error.html", error=error, errorcode=i), i
