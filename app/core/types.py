from __future__ import annotations

import typing as tp

from django.db.models import Model
from django.http import HttpRequest

from app.users.models import User

from django_filters import FilterSet
from rest_framework.serializers import Serializer

DjangoModel = tp.TypeVar('DjangoModelType', bound=Model)

DRFSerializer = tp.TypeVar('DRFSerializerType', bound=Serializer)

ErrorDetails = dict[str, tp.Any] | str | list[tp.Any]

DjangoFilter = tp.TypeVar('DjangoFilter', bound=FilterSet)

class AuthenticatedRequest(HttpRequest):
    user: User
