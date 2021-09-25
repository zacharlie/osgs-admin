from flask import flash
import subprocess
import json

import ruamel.yaml


def hello_world():
    flash("hw", "error")
    return "Hello World!"


def hello_sleepy_world():
    response = subprocess.run(
        ["bash", "-c", "echo Hello && sleep 10 && echo World"],
        # ["echo", "Hello", "&&", "sleep", "10", "&&", "echo", "World!"],
        shell=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.DEVNULL,
    ).stdout
    return response


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


def read_yaml(input_file):
    yaml = ruamel.yaml.YAML(typ="rt")  # roundtrip
    yaml.allow_duplicate_keys = True
    yaml.preserve_quotes = True
    doc = yaml.load(input_file)
    return doc


def write_yaml(data, output_file):
    yaml = ruamel.yaml.YAML(typ="rt")  # roundtrip
    yaml.default_flow_style = False
    yaml.preserve_quotes = True
    yaml.allow_duplicate_keys = True
    yaml.dump(data, output_file)
