import os
import sys

import pytest

# Make the `app` package importable when pytest is run from any folder
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.app import app as flask_app  # noqa: E402


@pytest.fixture
def client():
    flask_app.config['TESTING'] = True
    with flask_app.test_client() as client:
        yield client
