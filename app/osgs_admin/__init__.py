from flask import Flask, g, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_required
from os import path, environ

db = SQLAlchemy()


def create_app(test_config=None):
    app = Flask(__name__)

    app.config.from_mapping(
        # app secret should be overridden by instance config
        SECRET_KEY="developmentkey",
        DATABASE=path.join(app.instance_path, "adminapp.sqlite"),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        # app.config.from_pyfile("config.py", silent=True)

        # app.config["SECRET_KEY"] = "fzHofj7khjMslfoTVU5OONxqkcmCYPxBE5BygBaW9zyqT"
        # generate randomised secret key for session signing. It may break active sessions
        # on reinstantiation of the app, and may be served better by a k8s secret or something.
        # At this point in time it seems reasonable to use a random key for user deploys,
        # but this needs to be consistent when using a load balancer or distributed deploy
        from .utils.sec import key_gen

        app.config["SECRET_KEY"] = key_gen(82)
        app.config["DATABASE_FILE"] = "db.sqlite"
        # db path uses sqlite:/// for relative and sqlite://// for absolute
        app.config["SQLALCHEMY_DATABASE_URI"] = (
            "sqlite:///" + app.config["DATABASE_FILE"]
        )
        app.config["SQLALCHEMY_ECHO"] = True
        app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

        app.app_dir = path.realpath(path.dirname(__file__))
        app.database_path = path.join(app.app_dir, app.config["DATABASE_FILE"])

        # set celery config
        app.config["RESULT_BACKEND"] = environ["CELERY_RESULT_BACKEND"]
        app.config["CELERY_BROKER_URL"] = environ["CELERY_BROKER_URL"]

    else:
        # load testing config
        app.config.update(test_config)

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

    # Bootstrap process for initiating new database
    @login_required
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
    db_exists = True if path.exists(database_path) else False
    return db_exists
