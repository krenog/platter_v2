import logging

from logger.store_request import get_request


def get_client_ip(request):
    if request is None:
        return ""
    client_ip = request.META.get('REMOTE_ADDR', '')
    if 'HTTP_X_FORWARDED_FOR' in request.META:
        client_ip += ' [%s]' % request.META['HTTP_X_FORWARDED_FOR']
    return client_ip


class AddDjangoRequestFilter(logging.Filter):  # pylint: disable=too-few-public-methods
    def filter(self, record):
        # Initialise custom fields to empty, so the formatter doesn't raise
        # an error if there is no request or user
        record.user = ''
        record.client_ip = ''

        request = get_request()

        if request is not None:
            record.user = request.user
            record.client_ip = get_client_ip(request)

        return True
