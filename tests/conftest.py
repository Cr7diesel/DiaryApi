import pytest
from pytest_factoryboy import register
from rest_framework.test import APIClient

from tests.factories import UserFactory, DiaryFactory, NoteFactory


register(UserFactory)
register(DiaryFactory)
register(NoteFactory)


@pytest.fixture()
def user(user_factory):
    return user_factory.create()


@pytest.fixture()
def user_client(user):
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture()
def guest_client():
    return APIClient()
