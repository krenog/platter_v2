import threading

THREAD_LOCAL = threading.local()


def get_request():
    """
    get earlier saved request from thread or None
    :return: earlier saved request or None
    """
    return getattr(THREAD_LOCAL, 'current_django_request', None)


def _set_request(value):
    """
    save request to thread
    :param value: request
    :return: None
    """
    THREAD_LOCAL.current_django_request = value


class StoreRequestMiddleware():  # pylint: disable=too-few-public-methods
    """ Middleware to store request that will be used for extending of logs records """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        _set_request(request)
        response = self.get_response(request)
        _set_request(None)
        return response
