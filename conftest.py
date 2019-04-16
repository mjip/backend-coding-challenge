from app import application
import pytest

@pytest.fixture
def app():
    app = create_app()
    return app
