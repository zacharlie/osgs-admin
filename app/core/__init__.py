from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
import os
import rq_dashboard

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)

    # app.config["SECRET_KEY"] = "fzHofj7khjMslfoTVU5OONxqkcmCYPxBE5BygBaW9zyqT"
    # generate randomised secret key for session signing. It may break active sessions
    # on reinstantiation of the app, and may be served better by a k8s secret or something.
    # At this point in time it seems reasonable to use a random key for user deploys,
    # but this needs to be consistent when using a load balancer or distributed deploy
    from .utils.sec import key_gen

    app.config["SECRET_KEY"] = key_gen(82)
    app.config["DATABASE_FILE"] = "db.sqlite"
    # db path uses sqlite:/// for relative and sqlite://// for absolute
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + app.config["DATABASE_FILE"]
    app.config["SQLALCHEMY_ECHO"] = True
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    app.app_dir = os.path.realpath(os.path.dirname(__file__))
    app.database_path = os.path.join(app.app_dir, app.config["DATABASE_FILE"])

    db.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = "auth.page_login"
    login_manager.init_app(app)

    from .models import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .auth import auth as auth_blueprint

    app.register_blueprint(auth_blueprint)

    from .main import main as main_blueprint

    app.register_blueprint(main_blueprint)

    from .ops import ops as ops_blueprint

    app.register_blueprint(ops_blueprint)

    from . import tasks

    # rq_dashboard.blueprint.before_request(bp_login_required)
    app.register_blueprint(rq_dashboard.blueprint, url_prefix="/jobs")

    # app.config["RQ_DASHBOARD_USERNAME"] = "admin"
    # app.config["RQ_DASHBOARD_PASSWORD"] = "admin"

    # Bootstrap process for initiating new database
    @app.route("/bootstrap", methods=["POST"])
    def page_bootstrap():
        from .models import init_db as initialize_database

        bootstrap = initialize_database(app.database_path)
        return bootstrap

    # This is just for frontend dev and should be disabled to force
    # a 405 when requested without posting the bootstrapping operation

    # @app.route("/bootstrap", methods=["GET"])
    # def page_bootstrap_dev():
    #     return render_template("bootstrap.html")

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

    for errorcode in [
        item
        for elem in [
            [400, 401],
            range(403, 406 + 1, 1),
            range(408, 418 + 1, 1),
            [422, 423, 424, 428, 429, 431, 451],
            range(500, 505, 1),
        ]
        for item in elem
    ]:
        # https://werkzeug-doc.readthedocs.io/en/latest/exceptions.html

        @app.errorhandler(errorcode)
        def error(error):
            return (
                render_template(
                    "error.html",
                    error_code=error.code,
                    error_description=error.description,
                    error_name=error.name,
                ),
                errorcode,
            )

    return app


@login_required
def bp_login_required():
    """Enforce "@login_required" on the before_request function of a blueprint"""
    return None


def check_db(database_path):
    db_exists = True if os.path.exists(database_path) else False
    return db_exists
