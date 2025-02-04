from __future__ import annotations

import typing as tp

from django.db.models import Model
from django.http import HttpRequest

from rest_framework.serializers import Serializer

DjangoModelType = tp.TypeVar('DjangoModelType', bound=Model)

DRFSerializer = tp.TypeVar('DRFSerializerType', bound=Serializer)

ErrorDetails = dict[str, tp.Any] | str | list[tp.Any]


class AuthenticatedRequest(HttpRequest):
    """
    A protocol like class for type hinting authenticated requests in Django,
    combining HttpRequest and custom authenticated user attributes.

    Attributes:
    -----------
        user: Users model, representing the authenticated user associated with the
        request.
    """

    ...
    # user: Users
