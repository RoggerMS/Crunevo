import os
import pytest
from flask import url_for
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
def admin_user(app):
    with app.app_context():
        User.query.delete()
        db.session.commit()
        u = User(username="admin", email="admin@example.com", role="admin")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
        return u


@pytest.fixture
def moderator_user(app):
    with app.app_context():
        u = User(username="mod", email="mod@example.com", role="moderator")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
        return u


@pytest.fixture
def editor_user(app):
    with app.app_context():
        u = User(username="edit", email="edit@example.com", role="editor")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
        return u


@pytest.fixture
def normal_user(app):
    with app.app_context():
        u = User(username="user", email="user@example.com")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
        return u.id


def login(client, email, password):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=True
    )


def test_requires_login(client):
    resp = client.get("/admin/")
    assert resp.status_code == 302
    assert "/login" in resp.headers["Location"]


def test_denies_non_admin(app, client, normal_user):
    login(client, "user@example.com", "secret")
    resp = client.get("/admin/", follow_redirects=False)
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")


def test_allows_admin(app, client, admin_user):
    login(client, "admin@example.com", "secret")
    resp = client.get("/admin/")
    assert resp.status_code == 200


def test_moderator_permissions(app, client, moderator_user):
    login(client, "mod@example.com", "secret")
    resp_notes = client.get("/admin/notes")
    assert resp_notes.status_code == 200
    resp_store = client.get("/admin/store")
    assert resp_store.status_code == 302


def test_editor_permissions(app, client, editor_user):
    login(client, "edit@example.com", "secret")
    resp_store = client.get("/admin/store")
    assert resp_store.status_code == 200
    resp_notes = client.get("/admin/notes")
    assert resp_notes.status_code == 302


def test_change_user_role(app, client, admin_user, normal_user):
    login(client, "admin@example.com", "secret")
    resp = client.post(
        f"/admin/users/{normal_user}/role",
        data={"role": "moderator"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    with app.app_context():
        user = User.query.get(normal_user)
        assert user.role == "moderator"
