from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.base_user import BaseUserManager
from django.db import transaction
from django.db.utils import IntegrityError
from django.forms import ValidationError
from django.utils.translation import gettext_lazy as _

from allauth.account.models import EmailAddress

if TYPE_CHECKING:
    from .models import User


class UsersManager(BaseUserManager):
    model: type[User]

    @transaction.atomic
    def create_user(
        self,
        email: str,
        password: str,
        **extra_fields,
    ) -> User:
        if not email:
            raise ValidationError(_('The Email must be set'))

        email = self.normalize_email(email).lower()
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        self._try_save_user(user)
        self._setup_user_email(user)
        return user

    @transaction.atomic
    def create_superuser(
        self,
        email: str,
        password: str,
        **extra_fields,
    ) -> User:
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValidationError(_('Superuser must have is_staff=True.'))

        if extra_fields.get('is_superuser') is not True:
            raise ValidationError(_('Superuser must have is_superuser=True.'))

        return self.create_user(email, password, **extra_fields)

    def _setup_user_email(self, user: User) -> None:
        email_address = EmailAddress(
            user=user,
            email=user.email,
            primary=True,
            verified=False,
        )
        email_address.save()
        EmailAddress.objects.fill_cache_for_user(user, [email_address])

    def _try_save_user(self, user: User) -> None:
        try:
            user.full_clean()
            user.save()
        except IntegrityError as e:
            if (
                'duplicate key value violates unique constraint "users_email_key"'
                in str(e)
            ):
                raise ValidationError(_('This email is already in use.'))

            raise ValidationError(_('Error while saving user.'))
