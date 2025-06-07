import os
import pytest
from crunevo.app import create_app

@pytest.fixture
def app(tmp_path):
    os.environ["DATABASE_DIR"] = str(tmp_path)
    application = create_app()
    application.config["TESTING"] = True
    application.config["WTF_CSRF_ENABLED"] = False
    return application

@pytest.fixture
def client(app):
    return app.test_client()

def test_store_page_loads(client):
    resp = client.get("/tienda/")
    assert resp.status_code == 200
