from osgs_admin import create_app

# from osgs_admin.tasks import make_celery
from os import environ

app = create_app()

environ["FLASK_ENV"] = "development"
# environ['FLASK_ENV'] = 'production'

if __name__ == "__main__":
    app.run(host="0.0.0.0")
else:
    application = app
