from watchdog.observers.polling import PollingObserver
from watchdog.events import PatternMatchingEventHandler
from pathlib import Path
import time
from os import environ as env


if __name__ == "__main__":
    patterns = ["*"]
    ignore_patterns = [
        # ignore pycache
        "__pycache__/",
        "*/__pycache__/",
        "*/*/__pycache__/",
        "*/*/*/__pycache__/",
        "*.py[cod]",
        "*/*.py[cod]",
        "*/*/*.py[cod]",
        "*/*/*/*.py[cod]",
    ]
    ignore_patterns.insert(
        0, "*reloader"
    )  # Note it is important to ignore the reloader file to prevent "modified file" recursion
    ignore_directories = False
    case_sensitive = True
    my_event_handler = PatternMatchingEventHandler(
        patterns, ignore_patterns, ignore_directories, case_sensitive
    )


application_root = Path(env["TARGET"])
reloader = application_root.joinpath("reloader")
application_path = application_root.as_posix()


def on_created(event):
    print(f"{event.src_path} has been created!")
    touch_reload()


def on_deleted(event):
    print(f"File / path deleted: {event.src_path}!")
    touch_reload()


def on_modified(event):
    print(f"{event.src_path} has been modified")
    touch_reload()


def on_moved(event):
    print(f"File moved {event.src_path} to {event.dest_path}")
    touch_reload()


def touch_reload():
    reloader.touch()


touch_reload()

my_event_handler.on_created = on_created
my_event_handler.on_deleted = on_deleted
my_event_handler.on_modified = on_modified
my_event_handler.on_moved = on_moved
go_recursively = True
my_observer = PollingObserver(timeout=1)
my_observer.schedule(my_event_handler, application_path, recursive=go_recursively)

print("Watcher ready")

my_observer.start()

try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    my_observer.stop()
    my_observer.join()
