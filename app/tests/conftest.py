import pytest

from app import create_app, db

@pytest.fixture
def app_context():
    app = create_app()
    with app.app_context():
        db.create_all()
        yield
        