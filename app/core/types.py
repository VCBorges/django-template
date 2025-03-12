from __future__ import annotations

import typing as tp

from django.db.models import Model
from django.http import HttpRequest

from app.core.filters import BaseFilterSet
from app.core.serializers import BaseSerializer

if tp.TYPE_CHECKING:
    from app.users.models import User

DjangoModelType = tp.TypeVar('DjangoModelType', bound=Model)

DRFSerializerType = tp.TypeVar('DRFSerializerType', bound=BaseSerializer)

ErrorDetails = dict[str, tp.Any] | str | list[tp.Any]

DjangoFilterType = tp.TypeVar('DjangoFilterType', bound=BaseFilterSet)


class AuthenticatedRequest(HttpRequest):
    user: User
