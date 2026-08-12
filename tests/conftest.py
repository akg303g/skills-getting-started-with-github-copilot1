import copy

from fastapi.testclient import TestClient

from src import app as app_module

BASE_ACTIVITIES = copy.deepcopy(app_module.activities)


def reset_activities():
    app_module.activities = copy.deepcopy(BASE_ACTIVITIES)


@pytest.fixture(autouse=True)
def restore_activities():
    reset_activities()
    yield
    reset_activities()


@pytest.fixture
def client():
    return TestClient(app_module.app)
