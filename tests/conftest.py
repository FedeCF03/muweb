"""Fixtures compartidas."""

from __future__ import annotations

import pytest

from app import create_app
from app.container import Services, services as get_services


@pytest.fixture()
def app():
    return create_app({"TESTING": True, "SECRET_KEY": "test"})


@pytest.fixture()
def svc(app) -> Services:
    with app.app_context():
        yield get_services()


@pytest.fixture()
def client(app):
    with app.test_client() as test_client:
        yield test_client
