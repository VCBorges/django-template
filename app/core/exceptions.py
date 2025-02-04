from __future__ import annotations

import typing as tp

from app.core.types import ErrorDetails

from django.shortcuts import get_object_or_404

class APIError(Exception):
    def __init__(
        self,
        *,
        status_code: int = 500,
        details: ErrorDetails | None = None,
    ) -> None:
        super().__init__(details)
        self.status_code = status_code
        self.details = details or 'A server error occurred.'


class ObjectDoesNotExist(APIError):
    DETAILS = 'Object does not exist.'
    STATUS_CODE = 404

    @tp.override
    def __init__(self, details: ErrorDetails | None = None,) -> None:
        super().__init__(status_code=self.STATUS_CODE, details=self.DETAILS)
