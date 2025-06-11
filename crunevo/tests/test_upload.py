import os
import io
import pytest

from crunevo.app import create_app
from crunevo.extensions import db
from crunevo.models.user import User


@pytest.fixture
def app(tmp_path):
    os.environ["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_path}/test.db"
    application = create_app()
    application.config["TESTING"] = True
    application.config["WTF_CSRF_ENABLED"] = False
    with application.app_context():
        db.create_all()
    return application


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def user(app):
    with app.app_context():
        User.query.delete()
        db.session.commit()
        u = User(username="tester", email="tester@example.com")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
        return u


def login(client, email, password):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=True
    )


def test_upload_requires_login(client):
    response = client.get("/upload")
    assert response.status_code == 302
    assert "/login" in response.headers["Location"]


def test_reject_invalid_extension(app, client, user):
    login(client, "tester@example.com", "secret")
    data = {
        "title": "note",
        "faculty": "Ciencias",
        "course": "Math",
        "description": "desc",
        "tags": "tag",
        "terms": "y",
        "note_file": (io.BytesIO(b"bad"), "malware.exe"),
    }
    resp = client.post(
        "/upload", data=data, content_type="multipart/form-data", follow_redirects=True
    )
    assert b"Solo se permiten archivos" in resp.data


def test_reject_large_file(app, client, user):
    login(client, "tester@example.com", "secret")
    big = io.BytesIO(b"0" * (21 * 1024 * 1024))
    data = {
        "title": "note",
        "faculty": "Ciencias",
        "course": "Math",
        "description": "desc",
        "tags": "tag",
        "terms": "y",
        "note_file": (big, "large.pdf"),
    }
    resp = client.post("/upload", data=data, content_type="multipart/form-data")
    assert resp.status_code == 413


def test_accept_valid_upload(app, client, user):
    login(client, "tester@example.com", "secret")
    data = {
        "title": "ok",
        "faculty": "Ciencias",
        "course": "Math",
        "description": "desc",
        "tags": "tag",
        "terms": "y",
        "note_file": (io.BytesIO(b"%PDF-1.4"), "doc.pdf"),
    }
    resp = client.post(
        "/upload", data=data, content_type="multipart/form-data", follow_redirects=True
    )
    assert b"Apunte subido exitosamente" in resp.data


def test_post_without_login(client):
    data = {
        "title": "note",
        "faculty": "Ciencias",
        "course": "Math",
        "description": "desc",
        "tags": "tag",
        "terms": "y",
        "note_file": (io.BytesIO(b"%PDF-1.4"), "doc.pdf"),
    }
    resp = client.post("/upload", data=data, content_type="multipart/form-data")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]
