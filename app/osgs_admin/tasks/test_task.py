from rq import Retry, get_current_job
from . import q
import requests
import time


def time_consuming_request(url: str = "https://wikipedia.org"):
    job = get_current_job()
    response = requests.get(url)
    total = 0
    count = len(response.text.split())
    for i, elem in enumerate(response.text.split()):
        time.sleep(1)
        print(f"{i}: {elem}")
        job.meta["progress"] = 100.0 * i / count
        job.save_meta()
        total += 1
    job.meta["progress"] = 100
    job.save_meta()
    return total


def report_success(job, connection, result, *args, **kwargs):
    return True


def report_failure(job, connection, type, value, traceback):
    return False


def do_something(queue=q, url: str = "https://google.com"):
    result = queue.enqueue(
        time_consuming_request,
        url,
        on_success=report_success,
        on_failure=report_failure,
        retry=Retry(max=3, interval=[10, 30, 60]),
    )
    return result
