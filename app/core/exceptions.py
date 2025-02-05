from __future__ import annotations

import typing as tp

from app.core.types import ErrorDetails


class APIError(Exception):
    STATUS_CODE = 500
    DETAILS = 'A server error occurred.'

    def __init__(
        self,
        *,
        status_code: int = 500,
        details: ErrorDetails | None = None,
    ) -> None:
        super().__init__(details)
        self.status_code = status_code or self.STATUS_CODE
        self.details = details or self.DETAILS


class ObjectDoesNotExist(APIError):
    STATUS_CODE = 404
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
    STATUS_CODE = 400
    
    @tp.override
    def __init__(
        self,
        details: tp.Mapping[str, tp.Any],
    ) -> None:
        super().__init__(
            status_code=self.STATUS_CODE,
            details=details,
        )
        
