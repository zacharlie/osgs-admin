# Operations utils
# mostly for testing and dev - a bunch need to become celery tasks

from flask import flash
import subprocess
import json

import ruamel.yaml  # Replace pyyaml and support quotes, comments, and literals

# import yaml  # Uses pyyaml, superseded by ruamel


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


## def read_yaml(input_file):  # Uses pyyaml, superseded by ruamel
##     with input_file as f:
##         # doc = yaml.load(f, Loader=yaml.BaseLoader)
##         # doc = yaml.load(f, Loader=yaml.SafeLoader)
##         # doc = yaml.load(f, Loader=yaml.FullLoader)
##         doc = yaml.load(f, Loader=yaml.UnsafeLoader)
##         return doc

## def write_yaml(data, output_file):  # Uses pyyaml, superseded by ruamel
##     with output_file as f:
##         yaml.dump(data, f, default_flow_style=False, sort_keys=False)
