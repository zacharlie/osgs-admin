import os
import tempfile

import pytest

from osgs_admin import create_app
from osgs_admin.models import init_db


@pytest.fixture
def client():
    db_fd, db_path = tempfile.mkstemp()
    app = create_app({"TESTING": True, "DATABASE": db_path})

    with app.test_client() as client:
        with app.app_context():
            init_db(db_path)
        yield client

    os.close(db_fd)
    os.unlink(db_path)


def login(client, username, password):
    return client.post(
        "/login", data=dict(username=username, password=password), follow_redirects=True
    )


def logout(client):
    return client.get("/logout", follow_redirects=True)


def test_login_logout(client):
    """Make sure login and logout works."""

    username = "admin"
    password = "admin"

    rv = login(client, username, password)
    assert b"Logout" in rv.data

    rv = logout(client)
    assert b"Login" in rv.data

    rv = login(client, f"{username}x", password)
    assert b"Invalid credentials." in rv.data

    rv = login(client, username, f"{password}x")
    assert b"Invalid credentials." in rv.data
