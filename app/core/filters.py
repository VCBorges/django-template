from app.core.exceptions import ValidationError

from django_filters import FilterSet


class BaseFilterSet(FilterSet):
    def is_valid(self, raise_exception: bool = False) -> bool:
        valid = super().is_valid()
        if not valid and raise_exception:
            raise ValidationError(self.errors)

        return valid
