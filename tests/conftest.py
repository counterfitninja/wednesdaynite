import os
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

import pytest


@pytest.fixture
def app(tmp_path, monkeypatch):
    monkeypatch.setenv("SECRET_KEY", "test-secret-key")
    monkeypatch.setenv("ADMIN_PASSWORD", "test-password")
    import app as application

    database = tmp_path / "test.db"
    monkeypatch.setattr(application, "DATABASE", str(database))
    application.app.config["DATABASE"] = str(database)
    application.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    application.init_db()
    yield application.app


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def db_path(app):
    return app.config.get("DATABASE", getattr(app, "DATABASE", None))


def csrf_token(client):
    response = client.get("/login")
    with client.session_transaction() as session:
        return session["_csrf_token"]


def login(client):
    token = csrf_token(client)
    response = client.post(
        "/login",
        data={"password": os.environ["ADMIN_PASSWORD"], "_csrf_token": token},
    )
    assert response.status_code in (301, 302)
    with client.session_transaction() as session:
        return session["_csrf_token"]


def connect(path):
    connection = sqlite3.connect(path)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection
