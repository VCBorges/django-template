from __future__ import annotations

import typing as tp

from django.db.models import Model
from django.http import HttpRequest

from app.core.filters import BaseFilterSet
from app.core.serializers import BaseSerializer
from app.users.models import User

DjangoModel = tp.TypeVar('DjangoModelType', bound=Model)

DRFSerializer = tp.TypeVar('DRFSerializerType', bound=BaseSerializer)

ErrorDetails = dict[str, tp.Any] | str | list[tp.Any]

DjangoFilter = tp.TypeVar('DjangoFilter', bound=BaseFilterSet)


class AuthenticatedRequest(HttpRequest):
    user: User
