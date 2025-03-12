from django.test import Client

from app.users.models import User

import pytest


@pytest.fixture
def user_password() -> str:
    return '123qaz123'


@pytest.fixture
def user(user_password: str):
    email = 'test@test.com'
    first_name = 'Test'
    user = User.objects.create_user(
        data={
            'email': email,
            'password': user_password,
            'first_name': first_name,
        }
    )
    return user


@pytest.fixture
def existent_user_email(user: User) -> str:
    return user.email


@pytest.fixture
def authenticated_client(
    user: User,
    user_password: str,
    client: Client,
) -> Client:
    client.login(
        email=user.email,
        password=user_password,
    )
    return client


@pytest.fixture
def client() -> Client:
    return Client()
