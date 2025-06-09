import os
import pytest

from crunevo.app import create_app
from crunevo.models import db


@pytest.fixture
def app(tmp_path):
    os.environ["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_path}/test.db"
    application = create_app()
    application.config["TESTING"] = True
    with application.app_context():
        db.create_all()
    yield application


def test_sqlalchemy_env(tmp_path):
    uri = f"sqlite:///{tmp_path}/override.db"
    os.environ["SQLALCHEMY_DATABASE_URI"] = uri
    application = create_app()
    assert application.config["SQLALCHEMY_DATABASE_URI"] == uri


def test_index_route(app):
    with app.test_client() as client:
        response = client.get("/")
        assert response.status_code == 200


def test_about_route(app):
    with app.test_client() as client:
        response = client.get("/about")
        assert response.status_code == 200
        assert "¿Qué es CRUNEVO?" in response.text

        home_resp = client.get("/")
        assert "Acerca de CRUNEVO" in home_resp.text
