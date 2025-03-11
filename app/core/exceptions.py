from __future__ import annotations

import typing as tp

from app.core.types import ErrorDetails

from rest_framework import status


class APIError(Exception):
    def __init__(
        self,
        *,
        status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR,
        details: ErrorDetails = 'A server error occurred.',
    ) -> None:
        super().__init__(details)
        self.status_code = status_code
        self.details = details


class ObjectDoesNotExist(APIError):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAILS = 'Object does not exist.'

    @tp.override
    def __init__(
        self,
        details: ErrorDetails | None = None,
    ) -> None:
        super().__init__(
            status_code=self.STATUS_CODE,
            details=details or self.DETAILS,
        )


class ValidationError(APIError):
    STATUS_CODE = status.HTTP_400_BAD_REQUEST

    @tp.override
    def __init__(
        self,
        details: ErrorDetails,
    ) -> None:
        super().__init__(
            status_code=self.STATUS_CODE,
            details=details,
        )
