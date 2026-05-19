import pytest
from rest_framework.test import APIClient
from model_bakery import baker

@pytest.fixture
def api_client():
    return APIClient()

@pytest.fixture
def user(db):
    return baker.make('accounts.User')

@pytest.fixture
def auth_client(api_client, user):
    api_client.force_authenticate(user=user)
    return api_client