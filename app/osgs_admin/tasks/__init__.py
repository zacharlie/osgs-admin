from celery import Celery, current_app

# from app import celery
from app import app

# from celery.bin import worker as celery_worker
from osgs_admin import create_app


def make_celery(app):
    celery = Celery(
        app.import_name,
        backend=app.config["RESULT_BACKEND"],
        broker=app.config["CELERY_BROKER_URL"],
        include=["osgs_admin.tasks"],
    )
    celery.conf.update(app.config)
    celery.autodiscover_tasks(["osgs_admin.tasks", "osgs_admin.tasks.utils"])
    # celery.autodiscover_tasks("osgs_admin")
    # celery.autodiscover_tasks("osgs_admin.tasks")

    # application = current_app._get_current_object()
    # worker = celery_worker.worker(app=application)
    # options = {
    #     "broker": app.config["CELERY_BROKER_URL"],
    #     "loglevel": "INFO",
    #     "traceback": True,
    # }

    # worker.run(**options)
    # worker = celery_worker.worker()
    # worker = celery_worker.worker(app)
    # worker.run(loglevel="INFO")

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


# app = create_app()
celery = make_celery(app)


"""
app = create_app()

celery = make_celery(app)
application = current_app._get_current_object()

worker = celery_worker.worker(application)
worker.run(loglevel="INFO")

# start celery workers
# spawn_celery_worker(app, "myworker")

"""
