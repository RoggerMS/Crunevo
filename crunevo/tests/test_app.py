import os
import pytest

from crunevo.app import create_app


@pytest.fixture
def app(tmp_path):
    os.environ["DATABASE_DIR"] = str(tmp_path)
    application = create_app()
    yield application


def test_railway_volume(tmp_path):
    os.environ.pop("DATABASE_DIR", None)
    os.environ["RAILWAY_VOLUME_MOUNT_PATH"] = str(tmp_path)
    application = create_app()
    with application.app_context():
        assert application.config["SQLALCHEMY_DATABASE_URI"].startswith("sqlite:///" + str(tmp_path))

def test_index_route(app):
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200


def test_about_route(app):
    with app.test_client() as client:
        response = client.get('/about')
        assert response.status_code == 200
