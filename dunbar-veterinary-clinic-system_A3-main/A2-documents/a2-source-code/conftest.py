"""pytest fixtures: an isolated Flask app with a temporary SQLite database."""

import os
import sys
import tempfile

import pytest

# allow `import app` regardless of where pytest is invoked from
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import app as app_module
import db as db_module


@pytest.fixture()
def app(tmp_path):
    db_path = str(tmp_path / "test_clinic.db")
    app_module.app.config.update(
        DATABASE=db_path,
        TESTING=True,
        SECRET_KEY="test",
    )
    db_module.init_db(db_path)
    with app_module.app.app_context():
        yield app_module.app
    # reset module-level app state for the next test
    app_module.app.config["DATABASE"] = os.environ.get(
        "DATABASE_PATH", os.path.join(os.path.dirname(app_module.__file__), "data", "clinic.db"))


@pytest.fixture()
def client(app):
    return app.test_client()
