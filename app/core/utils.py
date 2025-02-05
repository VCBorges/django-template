from __future__ import annotations

from typing import TYPE_CHECKING

from django.db.models.query import QuerySet

from app.core.exceptions import ObjectDoesNotExist

if TYPE_CHECKING:
    from app.core.types import DjangoModel


def get_object_or_404(
    model_or_queryset: type[DjangoModel] | QuerySet[DjangoModel],
    *,
    pk: str,
    error_details: str | None = None,
) -> DjangoModel:
    if issubclass(model_or_queryset, DjangoModel):
        model_or_queryset = model_or_queryset.objects.all()
    try:
        return model_or_queryset.get(pk=pk)
    except model_or_queryset.DoesNotExist:
        raise ObjectDoesNotExist(error_details)
