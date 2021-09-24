from logging import info
from . import redis, q
from rq import Worker, exceptions
from rq.job import Job


def get_rq_workers(queue=q):
    workers = Worker.all(queue=q)
    return workers


def get_rq_job(job_id):
    try:
        rq_job = Job.fetch(job_id, connection=redis)
    except (exceptions.RedisError, exceptions.NoSuchJobError):
        return None
    return rq_job
