from . import celery

"""workers may be running from different containers,
so explicit task names should always be defined"""


@celery.task(name="osgs_admin.tasks.utils.add_together")
def add_together(a, b):
    return a + b


@celery.task(bind=True, name="osgs_admin.tasks.utils.long_task")
def long_task(self):
    import time
    import random

    """Background task that runs a long function with progress reports."""
    verb = ["Starting up", "Booting", "Repairing", "Loading", "Checking"]
    adjective = ["master", "radiant", "silent", "harmonic", "fast"]
    noun = ["solar array", "particle reshaper", "cosmic ray", "orbiter", "bit"]
    message = ""
    total = random.randint(10, 50)
    for i in range(total):
        if not message or random.random() < 0.25:
            message = "{0} {1} {2}...".format(
                random.choice(verb), random.choice(adjective), random.choice(noun)
            )
        self.update_state(
            state="PROGRESS", meta={"current": i, "total": total, "status": message}
        )
        time.sleep(5)
    return {"current": 100, "total": 100, "status": "Task completed!", "result": 42}
