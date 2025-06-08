import os
import pytest
from crunevo.app import create_app
from crunevo.models import db
from crunevo.models.user import User
from crunevo.models.forum import Pregunta


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
def user_id(app):
    with app.app_context():
        User.query.delete()
        db.session.commit()
        u = User(username="tester", email="tester@example.com")
        u.set_password("secret")
        db.session.add(u)
        db.session.commit()
        return u.id


def login(client, email, password):
    return client.post(
        "/login", data={"email": email, "password": password}, follow_redirects=True
    )


def test_forum_page_loads(client):
    resp = client.get("/foro/")
    assert resp.status_code == 200


def test_create_question(app, client, user_id):
    login(client, "tester@example.com", "secret")
    data = {
        "titulo": "Pregunta prueba",
        "contenido": "Contenido suficiente para probar la creación de preguntas",
    }
    resp = client.post("/foro/nueva", data=data, follow_redirects=True)
    assert b"Pregunta publicada" in resp.data
    with app.app_context():
        assert Pregunta.query.count() == 1
        q = Pregunta.query.first()
        assert q.autor_id == user_id


def test_add_response(app, client, user_id):
    with app.app_context():
        q = Pregunta(
            titulo="Titulo",
            contenido="Contenido de prueba suficientemente largo",
            autor_id=user_id,
        )
        db.session.add(q)
        db.session.commit()
        q_id = q.id
    login(client, "tester@example.com", "secret")
    data = {
        "contenido": "Esta es una respuesta suficientemente larga para pasar el filtro"
    }
    resp = client.post(f"/foro/{q_id}/responder", data=data, follow_redirects=True)
    assert b"Respuesta enviada" in resp.data
    resp = client.get(f"/foro/pregunta/{q_id}")
    assert b"suficientemente larga" in resp.data
