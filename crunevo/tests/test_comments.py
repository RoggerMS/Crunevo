import os
import pytest
from crunevo.app import create_app
from crunevo.extensions import db
from crunevo.models.user import User
from crunevo.models.note import Note


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
        u = User(username="cuser", email="cuser@example.com")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
        return u.id


def login(client, email, password):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=True
    )


def test_add_comment(app, client, user):
    with app.app_context():
        note = Note(
            title="t",
            description="d",
            file_url="/f.pdf",
            file_type="pdf",
            user_id=user,
        )
        db.session.add(note)
        db.session.commit()
        note_id = note.id
    login(client, "cuser@example.com", "secret")
    resp = client.post("/comments/add", data={"note_id": note_id, "content": "hola"})
    assert resp.status_code == 302
    with app.app_context():
        assert Note.query.get(note_id).comments[0].content == "hola"
