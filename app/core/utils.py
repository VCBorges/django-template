from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models.query import QuerySet

from app.core.exceptions import ObjectDoesNotExist

if TYPE_CHECKING:
    from app.core.types import DjangoModelType


def get_object_or_404(
    model_or_queryset: type[DjangoModelType] | QuerySet[DjangoModelType],
    *,
    pk: str,
    error_details: str | None = None,
) -> DjangoModelType:
    if issubclass(model_or_queryset, DjangoModelType):
        model_or_queryset = model_or_queryset.objects.all()
    try:
        return model_or_queryset.get(pk=pk)
    except model_or_queryset.DoesNotExist:
        raise ObjectDoesNotExist(error_details)
