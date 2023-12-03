import pytest
from django.contrib.auth.models import User
from django.test import Client


@pytest.fixture
def user():
    return User.objects.create_user(username='testuser', password='testpassword')


@pytest.fixture
def client():
    return Client()


@pytest.fixture
def authenticate(user, client):
    client.login(username='testuser', password='testpassword')
