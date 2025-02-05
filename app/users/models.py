from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.db import models
from django.utils.translation import gettext_lazy as _

from app.users.managers import UsersManager


class User(
    AbstractBaseUser,
    PermissionsMixin,
):
    email = models.EmailField(_('email address'), unique=True)
    first_name = models.CharField(_('first name'), max_length=30, blank=True)
    last_name = models.CharField(_('last name'), max_length=30, blank=True)
    birth_date = models.DateField(_('birth date'), blank=True, null=True)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    joined_at = models.DateTimeField(auto_now_add=True)
    height = models.IntegerField(_('height'), blank=True, null=True)
    weight = models.IntegerField(_('weight'), blank=True, null=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        db_table = 'users'

    USERNAME_FIELD = 'email'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    objects: UsersManager = UsersManager()

    def __str__(self):
        return f'<{self.__class__.__name__} (email="{self.email}")>'
