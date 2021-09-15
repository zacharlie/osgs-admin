# Operations

import os
from .models import Osgs

import subprocess

osgs = Osgs.query.all()[0]


def clone_stackroot(osgs):
    subprocess.run(
        ["git", "clone", osgs.config["targetrepo"], osgs.stackroot],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout


def run_make(osgs):
    return subprocess.run(
        ["make", "-s", "-C", osgs.stackroot],
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout
