from __future__ import annotations

import typing as tp

from django import forms
from django.http import HttpRequest

from app.core.exceptions import ValidationError

if tp.TYPE_CHECKING:
    from app.core.types import DjangoModelType


# TODO: Remove any renderable feature.
class BaseForm(forms.Form):
    normalized_fields_mapping = {}

    @tp.override
    def __init__(
        self,
        *args,
        **kwargs,
    ) -> None:
        self.request: HttpRequest | None = kwargs.pop('request', None)
        self.instance: DjangoModelType | None = kwargs.pop('instance', None)
        super().__init__(*args, **kwargs)

    def normalize_cleaned_data(self) -> dict[str, tp.Any]:
        for key, value in self.normalized_fields_mapping.items():
            if key in self.cleaned_data:
                self.cleaned_data[value] = self.cleaned_data.pop(key)

    @tp.override
    def clean(self) -> dict[str, tp.Any]:
        data = super().clean()
        self.normalize_cleaned_data()
        return data

    @tp.override
    def is_valid(self, *, raise_exception: bool = True) -> bool:
        valid = super().is_valid()

        if not valid and raise_exception:
            raise ValidationError(self.errors)

        return valid
