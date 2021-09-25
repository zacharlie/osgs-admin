from osgs_admin import create_app

# from osgs_admin.tasks import make_celery
from os import environ

app = create_app()
# celery = make_celery(app)
# worker = celery.Worker(include=["osgs_admin.tasks"])
# worker.start()
# worker = celery.Worker(include=["osgs_admin.tasks"])
# worker.start()
# worker.start(argv=['celery', 'worker', '-l', 'info'])
# celery.worker_main(argv=["worker", "--loglevel=info"])
# celery.worker_main(argv=["worker", "--loglevel=info", "--detach"])
"""
import threading

threading.Thread(
    # target=celery.worker_main, args=("worker", "--loglevel=info"), daemon=True
    target=celery.worker_main,
    args=("worker", "--loglevel=info"),
)
"""

# environ["FLASK_ENV"] = "development"
# environ['FLASK_ENV'] = 'production'

if __name__ == "__main__":
    app.run(host="0.0.0.0")
else:
    application = app
