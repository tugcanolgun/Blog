import logging

import pytest
from django.test import Client
from django.contrib.auth.models import User

from panel.factories import UserFactory


@pytest.fixture(autouse=True)
def disable_loggers() -> None:
    logging.disable(logging.CRITICAL)
    yield
    logging.disable(logging.NOTSET)


@pytest.fixture
def client() -> Client:
    return Client()


@pytest.fixture
def user() -> User:
    return UserFactory()


@pytest.fixture
def user_client(client: Client, user: User) -> Client:
    client.login(username=user.username, password="p@ssw0rd")

    return client
