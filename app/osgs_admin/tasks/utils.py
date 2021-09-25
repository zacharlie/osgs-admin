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
        time.sleep(1)
    return {"current": 100, "total": 100, "status": "Task completed!", "result": 42}


'''
from psutil import Process
from subprocess import Popen
import shlex


def start_celery():
    """
    Start the celery deamon.
    @returns:
      subprocess.Popen object that supports pid lookup via
      self.pid
    """
    cmd = "celery worker "
    cmd += "--app intertext.tasks "
    cmd += "--loglevel error"
    return Popen(shlex.split(cmd))


def terminate_process(pid):
    """
    Stop a process given its pid or stop all processes if pid
    is a list of identifiers.
    @args:
      int pid: the process identifier of the root process that
        spawned child celery processes
    """
    process = Process(pid)
    for child in process.children(recursive=True):
        child.kill()
    process.kill()


# main
celery_process = start_celery()

# ...do work... then
terminate_process(celery_process.pid)
'''
