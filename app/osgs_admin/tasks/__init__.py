from celery import Celery
from app import app


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
        include=["osgs_admin.tasks"],
    )
    celery.conf.update(app.config)

    # register all the classes celery will process
    celery.autodiscover_tasks(["osgs_admin.tasks", "osgs_admin.tasks.utils"])

    class ContextTask(celery.Task):
        def __call__(self, *args, **kwargs):
            with app.app_context():
                return self.run(*args, **kwargs)

    celery.Task = ContextTask
    return celery


def spawn_celery_worker(app, worker_name):
    import subprocess

    output = subprocess.run(
        [
            "bash",
            "-c",
            f"celery -A {app.import_name}.tasks.celery worker --loglevel=INFO --concurrency=10 -n {worker_name}@flask",
        ],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout
    return output


# Use app context and celery factory to define
# celery object for use as the app task decorator
celery = make_celery(app)
