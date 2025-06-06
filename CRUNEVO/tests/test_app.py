import os
import sys
import pytest

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crunevo.app import create_app

def test_index_route():
    app = create_app()
    with app.test_client() as client:
        response = client.get('/')
        assert response.status_code == 200
