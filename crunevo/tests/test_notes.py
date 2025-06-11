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
def admin_user(app):
    with app.app_context():
        User.query.delete()
        db.session.commit()
        u = User(username="admin", email="admin@example.com", role="admin")
        u.set_password("admin123")
        db.session.add(u)
        db.session.commit()
        return u


def login(client, email, password):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=True
    )


def test_admin_notes_no_error(client, admin_user):
    login(client, "admin@example.com", "admin123")
    resp = client.get("/admin/notes")
    assert resp.status_code == 200
