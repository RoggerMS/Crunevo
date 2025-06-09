import os
import pytest
from crunevo.app import create_app
from crunevo.models import db
from crunevo.models.user import User
from crunevo.models.log import LoginLog


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


def test_login_log_created(app, client):
    with app.app_context():
        u = User(username="tester", email="tester@example.com")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
    resp = client.post(
        "/login",
        data={"email": "tester@example.com", "password": "secret"},
        follow_redirects=True,
    )
    assert resp.status_code == 200
    with app.app_context():
        assert LoginLog.query.count() == 1
        log = LoginLog.query.first()
        assert log.success is True
