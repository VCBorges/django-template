from __future__ import annotations, unicode_literals

import json
import logging
import typing as tp

from django.db.models.query import QuerySet
from django.forms import ValidationError as DjangoValidationError
from django.http import HttpRequest, JsonResponse, QueryDict
from django.template.response import TemplateResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from app.core.exceptions import APIError, ValidationError
from app.core.types import DjangoFilter, DjangoModel, DRFSerializer
from app.core.utils import get_object_or_404

from rest_framework.exceptions import ValidationError as DRFValidationError

logger = logging.getLogger(__name__)

HTTPMethod = tp.Literal['post', 'get', 'put', 'delete']

Response = JsonResponse | TemplateResponse


class APIView(View):
    http_method_names: list[HTTPMethod] = []
    model: type[DjangoModel] | None = None
    queryset: QuerySet[DjangoModel] | None = None
    pk_url_kwarg = 'pk'
    template_engine: str = 'django'

    request: HttpRequest
    object: DjangoModel | None = None
    data: tp.Mapping[str, tp.Any] | QueryDict
    kwargs: tp.Mapping[str, tp.Any]

    def parse_json_body(self) -> dict[str, tp.Any]:
        if self.request.body == b'':
            return {}

        try:
            data = json.loads(self.request.body.decode())
            return data

        except json.JSONDecodeError as error:
            logger.exception(error)
            raise APIError(
                status_code=400,
                details=self.error_dict(str(error)),
            )

    def get_validated_body(
        self,
        serializer_class: type[DRFSerializer],
    ) -> dict[str, tp.Any]:
        serializer = serializer_class(data=self.data)
        try:
            serializer.is_valid(raise_exception=True)
        except DRFValidationError as error:
            logger.exception(error)
            raise ValidationError(error.detail)

        return serializer.validated_data

    def get_serialized_queryset(
        self,
        serializer_class: type[DRFSerializer],
        queryset: QuerySet[DjangoModel],
    ) -> dict[str, tp.Any]:
        serializer = serializer_class(queryset, many=True)
        return serializer.data

    def get_filtered_queryset(
        self,
        filter_class: type[DjangoFilter],
        queryset: QuerySet[DjangoFilter],
    ) -> QuerySet[DjangoModel]:
        filter = filter_class(
            data=self.data,
            queryset=queryset,
        )
        filter.is_valid(raise_exception=True)
        return filter.qs

    def get_request_data(self) -> tp.Mapping[str, tp.Any] | QueryDict:
        if self.request.method in [
            'GET',
            'HEAD',
        ]:
            return self.request.GET

        if self.request.content_type == 'application/json':
            return self.parse_json_body()

        return self.request.POST | self.request.FILES

    @tp.override
    def get_object(self) -> DjangoModel | None:
        if self.queryset or self.model:
            return get_object_or_404(
                self.queryset or self.model,
                pk=self.kwargs.get(self.pk_url_kwarg),
            )

        return None

    @tp.override
    def dispatch(self, *args: tp.Any, **kwargs: tp.Any) -> JsonResponse:
        try:
            self.data = self.get_request_data()
            self.object = self.get_object()
            response = super().dispatch(*args, **kwargs)
        except Exception as exc:
            response = self.handle_exception(exc)
        return response

    def handle_exception(self, exception: Exception) -> JsonResponse:
        if isinstance(exception, APIError):
            return self.render_to_json(
                status_code=exception.status_code,
                data=self.error_dict(exception.details),
            )

        if isinstance(exception, DjangoValidationError):
            return self.render_to_json(
                status_code=400,
                data=self.error_dict(exception.error_dict),
            )

        if isinstance(exception, DRFValidationError):
            return self.render_to_json(
                status_code=400,
                data=self.error_dict(exception.detail),
            )

        return self.render_to_json(
            status_code=500,
            data=self.error_dict('Server error ocurred.'),
        )

    def render_to_json(
        self,
        *,
        data: dict[str, tp.Any] | None = None,
        status_code: int = 200,
    ) -> JsonResponse:
        if data is None:
            data = {}

        return JsonResponse(
            data=data,
            status=status_code,
            json_dumps_params={'ensure_ascii': False},
        )

    def error_dict(
        self,
        details: tp.Mapping[str, tp.Any] | str,
    ) -> dict[str, tp.Any]:
        return {'errors': details}

    def render_to_template(
        self,
        template: str,
        context: dict[str, tp.Any] | None = None,
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

    def get_context_data(self, **kwargs) -> dict[str, tp.Any]:
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
