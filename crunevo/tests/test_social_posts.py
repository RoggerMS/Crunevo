import os
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
        u = User(username="poster", email="poster@example.com")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
        return u


def login(client, email, password):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=True
    )


def test_create_post(client, user):
    login(client, "poster@example.com", "secret")
    resp = client.post("/crear_post", data={"content": "hola"})
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")
