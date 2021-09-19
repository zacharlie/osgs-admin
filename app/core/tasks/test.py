from rq import Retry
from . import q

from .example import time_consuming_request


def report_success(job, connection, result, *args, **kwargs):
    return True


def report_failure(job, connection, type, value, traceback):
    return False


# result = q.enqueue(
#     time_consuming_request,
#     "https://google.com",
#     on_success=report_success,
#     on_failure=report_failure,
#     retry=Retry(max=3, interval=[10, 30, 60]),
#     kwargs={"description": "Time consuming request example"},
# )

result = q.enqueue(
    time_consuming_request,
    "https://google.com",
    on_success=report_success,
    on_failure=report_failure,
    retry=Retry(max=3, interval=[10, 30, 60]),
)
