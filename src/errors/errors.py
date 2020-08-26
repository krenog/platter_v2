from django.utils.translation import gettext_lazy as _
from rest_framework import status
from rest_framework.exceptions import APIException


class ThirdPartyAPIError(APIException):
    status_code = status.HTTP_502_BAD_GATEWAY
    default_detail = _('Server Error')
    default_code = 'server_error'

    def __init__(self, detail=None, code=None):
        super().__init__(detail, code)
