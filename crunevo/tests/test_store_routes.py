import os
import pytest
from crunevo.app import create_app


@pytest.fixture
def app(tmp_path):
    os.environ["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{tmp_path}/test.db"
    application = create_app()
    application.config["TESTING"] = True
    application.config["WTF_CSRF_ENABLED"] = False
    with application.app_context():
        from crunevo.extensions import db

        db.create_all()
    return application


@pytest.fixture
def client(app):
    return app.test_client()


def test_store_page_loads(client):
    resp = client.get("/tienda/")
    assert resp.status_code == 200
