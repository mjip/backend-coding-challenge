from app import application
import pytest

@pytest.fixture
def app():
    app = create_app()
    return app

@pytest.fixture
def conf_test():
	return "Configured!"
