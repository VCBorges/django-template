import json
from urllib.parse import urlencode

from django.test.client import RequestFactory

from app.core.exceptions import APIError, ValidationError
from app.core.serializers import BaseSerializer
from app.core.views import APIView

import pytest
from rest_framework import serializers


class DummySerializer(BaseSerializer):
    name = serializers.CharField(required=True)


class DummyAPIView(APIView):
    http_method_names = ['get']

    def get(self, request, *args, **kwargs):
        return self.render_to_json(data={'message': 'success'})


def test_parse_json_body_success(rf: RequestFactory):
    data = {'key': 'value'}
    body = json.dumps(data)
    request = rf.post(
        '/dummy',
        data=body,
        content_type='application/json',
    )

    view = APIView()
    view.request = request
    result = view.parse_json_body()
    assert result == data


def test_parse_json_body_empty(rf: RequestFactory):
    request = rf.post(
        '/dummy',
        data=b'',
        content_type='application/json',
    )

    view = APIView()
    view.request = request
    result = view.parse_json_body()
    assert result == {}


def test_parse_json_body_invalid(rf: RequestFactory):
    # Simulate a POST request with invalid JSON
    request = rf.post(
        '/dummy',
        data='invalid json',
        content_type='application/json',
    )

    view = APIView()
    view.request = request
    with pytest.raises(APIError) as exc_info:
        view.parse_json_body()
    assert exc_info.value.status_code == 400


def test_get_request_data_get(rf: RequestFactory):
    request = rf.get('/dummy?foo=bar')

    view = APIView()
    view.request = request
    data = view.get_request_data()
    assert data['foo'] == 'bar'


def test_get_request_data_json(rf: RequestFactory):
    # Test POST request with JSON content
    payload = {'foo': 'bar'}
    body = json.dumps(payload)
    request = rf.post('/dummy', data=body, content_type='application/json')

    view = APIView()
    view.request = request
    data = view.get_request_data()
    assert data == payload


def test_get_request_data_post_form(rf: RequestFactory):
    query_string = urlencode({'foo': 'bar'})

    request = rf.post(
        '/dummy',
        data=query_string,
        content_type='application/x-www-form-urlencoded',
    )

    view = APIView()
    view.request = request
    returned_data = view.get_request_data()

    assert returned_data['foo'][0] == 'bar'


def test_dispatch_get(rf: RequestFactory):
    request = rf.get('/dummy')

    view_instance = DummyAPIView()
    view_instance.request = request
    view_instance.kwargs = {}

    response = view_instance.dispatch(request, **view_instance.kwargs)

    # Verify the response is as expected
    assert response.status_code == 200
    result = json.loads(response.content)
    assert result['message'] == 'success'


def test_get_validated_input_success():
    view = APIView()
    view.data = {'name': 'John Doe'}

    validated_data = view.get_validated_input(DummySerializer)

    assert validated_data == {'name': 'John Doe'}


def test_get_validated_input_invalid():
    view = APIView()
    view.data = {}

    with pytest.raises(ValidationError) as exc_info:
        view.get_validated_input(DummySerializer)

    error_detail = exc_info.value.args[0]
    assert 'name' in error_detail


