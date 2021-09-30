# authentication and security utils

from os import urandom
from base64 import b64encode
from random import randint


def key_gen(int: int):
    """Generate a random-ish key

    base64 encoded to remove escape chars and produce a string
    value from the random binary. Trimmed to increase entropy
    and ensure padding characters are excluded"""
    if int > 100 or int < 12:
        raise ValueError("Only keys of 12-100 chars supported")
    start = randint(5, 25)
    end = start + int
    key = b64encode(urandom(150)).decode("utf-8")[start:end]
    return key
