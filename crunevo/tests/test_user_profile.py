import os
import pytest
from crunevo.app import create_app
from crunevo.extensions import db
from crunevo.models.user import User
from crunevo.models.note import Note
from crunevo.models.forum import Pregunta, Respuesta


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
def sample_user(app):
    with app.app_context():
        u = User(username="tester", email="tester@example.com")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
        return u.id


def login(client, email, password):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=False
    )


def test_profile_page_shows_stats(client, app, sample_user):
    with app.app_context():
        uid = sample_user
        n = Note(title="Algebra", file_url="/a.pdf", user_id=uid)
        n.downloads_count = 3
        n.likes_count = 2
        db.session.add(n)
        q = Pregunta(titulo="Metodo?", contenido="desc", autor_id=uid)
        db.session.add(q)
        r = Respuesta(contenido="respuesta", autor_id=uid, pregunta=q)
        db.session.add(r)
        db.session.commit()
    login(client, "tester@example.com", "secret")
    resp = client.get("/user/profile")
    assert resp.status_code == 200
    assert b"Apuntes subidos" in resp.data
    assert b"Descargas totales" in resp.data
    assert b"Algebra" in resp.data
