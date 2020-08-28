import functools

import marshmallow
from django import http
from marshmallow import EXCLUDE

from errors.errors import ClientError


def validate_request(*, schema=None):
    """Request validate decorator
    """

    schema_instance = schema() if schema is not None else None

    def _decorator(view):
        @functools.wraps(view)
        def _view(request: http.HttpRequest, *args, **kwargs):
            request.SCHEMA_POST = schema_instance
            try:
                result = schema_instance.load(request.data,unknown=EXCLUDE)
            except marshmallow.exceptions.ValidationError as error:
                raise ClientError(
                    code='validation_error',
                    detail=error.messages,
                )
            request.VALIDATED_DATA = result
            return view(request, *args, **kwargs)

        return _view

    return _decorator
