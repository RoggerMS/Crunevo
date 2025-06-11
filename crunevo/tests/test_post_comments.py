import os
import pytest
from crunevo.app import create_app
from crunevo.extensions import db
from crunevo.models.user import User
from crunevo.models.post import Post
from crunevo.models.post_comment import PostComment


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
        u = User(username="cposter", email="cposter@example.com")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
        return u.id


def login(client, email, password):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=True
    )


def test_comment_post(client, user, app):
    with app.app_context():
        p = Post(content="hola", user_id=user)
        db.session.add(p)
        db.session.commit()
        post_id = p.id
    login(client, "cposter@example.com", "secret")
    resp = client.post(f"/posts/{post_id}/comment", data={"content": "ok"})
    assert resp.status_code == 302
    with app.app_context():
        assert PostComment.query.filter_by(post_id=post_id).count() == 1
