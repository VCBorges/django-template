from __future__ import annotations, unicode_literals

import json
import logging
import typing as tp
from typing import Any, Literal, Mapping

from django.db.models.query import QuerySet
from django.http import HttpRequest, JsonResponse, QueryDict
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.core.exceptions import APIError
from app.core.types import DjangoModelType, DRFSerializer

from apps.core.utils import get_or_404

logger = logging.getLogger(__name__)

HTTPMethod = Literal['post', 'get', 'put', 'delete']

Response = JsonResponse | TemplateResponse


class APIView(View):
    http_method_names: list[HTTPMethod] = []
    request: HttpRequest
    model: type[DjangoModelType] | None = None
    queryset: QuerySet[DjangoModelType] | None = None
    object: DjangoModelType | None = None
    data: Mapping[str, Any] | QueryDict
    pk_url_kwarg = 'pk'
    kwargs: dict[str, Any]
    template_engine: str = 'django'

    def _parse_json_body(self) -> dict[str, tp.Any]:
        if self.request.body == b'':
            return {}

        try:
            data = json.loads(self.request.body.decode('utf-8'))
            return data

        except json.JSONDecodeError as error:
            logger.exception(error)
            raise APIError(
                status_code=400,
                details=self._error_dict(str(error)),
            )

    def get_validated_input(
        self,
        serializer_class: type[DRFSerializer],
    ) -> dict[str, Any]:
        serializer = serializer_class(data=self.data)
        serializer.is_valid(raise_exception=True)
        return serializer.validated_data

    def _get_request_data(self) -> Mapping[str, tp.Any] | QueryDict:
        if self.request.method in [
            'GET',
            'POST',
        ]:
            return getattr(self.request, self.request.method)

        if self.request.content_type == 'application/json':
            return self._parse_json_body()

        return self.request.POST | self.request.FILES

    @tp.override
    def get_object(self) -> DjangoModelType | None:
        if self.queryset or self.model:
            return get_or_404(
                self.queryset or self.model,
                pk=self.kwargs.get(self.pk_url_kwarg),
            )

        return None

    @tp.override
    def setup(self, request: HttpRequest, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.data = self._get_request_data()
        self.object = self.get_object()

    @tp.override
    def dispatch(self, *args: Any, **kwargs: Any) -> JsonResponse:
        try:
            response = super().dispatch(*args, **kwargs)
        except Exception as error:
            response = self.handle_exception(error)
        return response

    # TODO: Handle DRF Serializer Validation Error
    def handle_exception(self, exception: Exception) -> JsonResponse:
        if isinstance(exception, APIError):
            return self.render_to_json(
                status_code=exception.status_code,
                data=self._error_dict(exception.details),
            )
        return self.render_to_json(status_code=500)

    def render_to_json(
        self,
        *,
        data: dict[str, Any] | None = None,
        status_code: int = 200,
    ) -> JsonResponse:
        if data is None:
            data = {}

        return JsonResponse(
            data=data,
            status=status_code,
            json_dumps_params={'ensure_ascii': False},
        )

    def _error_dict(
        self,
        details: Mapping[str, tp.Any] | str,
    ) -> dict[str, tp.Any]:
        return {'errors': details}

    def render_to_template(
        self,
        template: str,
        context: dict[str, Any] | None = None,
        status_code: int = 200,
        **response_kwargs,
    ) -> TemplateResponse:
        if context is None:
            context = {}

        response_kwargs.setdefault('content_type', self.request.content_type)
        return TemplateResponse(
            request=self.request,
            status=status_code,
            template=template,
            context=self.get_context_data(**context),
            using=self.template_engine,
            **response_kwargs,
        )

    def get_context_data(self, **kwargs) -> dict[str, Any]:
        kwargs.setdefault('view', self)
        return kwargs

    def post(self, *args, **kwargs) -> Response:
        raise NotImplementedError

    def get(self, *args, **kwargs) -> Response:
        raise NotImplementedError

    def put(self, *args, **kwargs) -> Response:
        raise NotImplementedError

    def delete(self, *args, **kwargs) -> Response:
        raise NotImplementedError


class CsrfExemptMixin:
    @method_decorator(csrf_exempt)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)
