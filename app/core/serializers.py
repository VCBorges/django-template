import typing as tp

from app.core.exceptions import ValidationError

from rest_framework import serializers


class BaseSerializer(serializers.Serializer):
    @tp.override
    def is_valid(self, *, raise_exception=False) -> bool:
        try:
            return super().is_valid(raise_exception=raise_exception)
        except serializers.ValidationError as error:
            raise ValidationError(error.detail)