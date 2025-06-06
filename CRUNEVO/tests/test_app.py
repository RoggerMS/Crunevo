import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crunevo.app import create_app


@pytest.fixture
def app():
    tmp_dir = os.path.join(os.getcwd(), "tmp_test_db")
    os.makedirs(tmp_dir, exist_ok=True)
    os.environ["DATABASE_DIR"] = tmp_dir
    application = create_app()
    yield application

def test_index_route(app):
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200


def test_about_route(app):
    with app.test_client() as client:
        response = client.get('/about')
        assert response.status_code == 200
