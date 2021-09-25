import json
import os
import sys

current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from utils import read_yaml, write_yaml


def get_user_config(root):
    config = os.path.join(root, "config/config.json")
    user_config = json.load(open(config))
    return user_config


def get_compose_config():
    compose_config = "/path/to/docker-compose.yaml"  # to get from config
    read_yaml(open(compose_config, "r"))


def set_compose_config(data):
    compose_config = "/path/to/docker-compose.yaml"
    write_yaml(data, open(compose_config, "w"))
