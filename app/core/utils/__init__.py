# Operations utils

import subprocess

import json


def hello_world():
    return "Hello World!"


def clone_root(osgs):

    osgs_repo = json.loads(osgs.config)["osgs_repo"]

    return subprocess.run(
        ["git", "clone", osgs_repo, osgs.root],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout


def run_make(osgs):
    return subprocess.run(
        ["make", "-s", "-C", osgs.root],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout
