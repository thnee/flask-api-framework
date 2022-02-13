import importlib
import sys

import pytest


@pytest.fixture(scope="function")
def examples_client(request):
    name = request.param[0]
    app_or_create_app = request.param[1]

    sys.path.append("examples")
    module = importlib.import_module(name)

    if app_or_create_app == "app":
        app = module.app
    elif app_or_create_app == "create_app":
        app = module.create_app(conf="test")

    with app.app_context():
        with app.test_client() as client:
            yield client

    del sys.modules[name]
    sys.path.remove("examples")
