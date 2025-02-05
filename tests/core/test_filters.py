from app.core.filters import BaseFilterSet

from django_filters import filters


def test_is_valid_to_raise_a_APIError_when_invalid() -> None:
    class TestFilter(BaseFilterSet):
        field1 = filters.CharFilter()
