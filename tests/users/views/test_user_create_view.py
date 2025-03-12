from django.test import Client
from django.urls import reverse

from app.users import models

import pytest
from allauth.account.models import EmailAddress


@pytest.mark.django_db
def test_to_create_a_new_user():
    url = reverse('create_list_users')
    Client().post(
        path=url,
        data={
            'first_name': 'Test',
            'email': 'test@test.com',
            'password1': '123qaz123',
            'password2': '123qaz123',
        },
        content_type='application/json',
    )
    assert models.User.objects.filter(email='test@test.com').exists()


@pytest.mark.django_db
def test_to_create_a_new_email_address():
    url = reverse('create_list_users')
    Client().post(
        path=url,
        data={
            'first_name': 'Test',
            'email': 'test@test.com',
            'password1': '123qaz123',
            'password2': '123qaz123',
        },
        content_type='application/json',
    )
    assert EmailAddress.objects.filter(email='test@test.com').exists()


