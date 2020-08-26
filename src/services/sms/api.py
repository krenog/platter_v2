import json
import time

import requests
from django.conf import settings
from django.core.serializers.json import DjangoJSONEncoder

from errors.errors import ThirdPartyAPIError
from logger.loggers import platter_logger
from services.session import get_session

logger = platter_logger()


def send_request(method='GET', params=None, data=None):
    session = get_session(settings.SMSTRAFFIC_URL, settings.SMSTRAFFIC_CONNECTION_POOL_SIZE)
    try:
        request = requests.Request(method, url=settings.SMSTRAFFIC_URL, params=params, data=data).prepare()
        message = dict(
            text='SMS traffic request.',
            request=json.dumps(data, cls=DjangoJSONEncoder),
        )
        logger.debug(json.dumps(message))
        response = session.send(request, timeout=settings.SMSTRAFFIC_TIMEOUT_SECONDS)
        logger.debug('SMS traffic response: %s %s', response.status_code, response.text)
        message = dict(
            text='SMS traffic response.',
            response_status=response.status_code,
            tesponse_text=response.text
        )
        logger.debug(json.dumps(message))

    except requests.RequestException as error:
        message = dict(
            text='SMS traffic RequestException',
            error=error,
        )
        logger.error(json.dumps(message))
        raise ThirdPartyAPIError(code='sms_traffic_unavailable')
    return response


def send_sms(phone_number: str, text: str):
    sms_result = False
    count_send_sms_code = 0

    data = dict(
        login=settings.SMSTRAFFIC_LOGIN,
        psw=settings.SMSTRAFFIC_PASSWORD,
        phones='7' + phone_number,
        mes=text,
    )
    while not sms_result and count_send_sms_code < 5:
        response = send_request(
            method='POST',
            data=data,
        )
        sms_result = response.status_code == 200
        count_send_sms_code += 1

        if not sms_result:
            logger.exception('SMS traffic error: %s', json.dumps(response, cls=DjangoJSONEncoder))
            message = dict(
                text='SMS traffic error ',
                error=json.dumps(response, cls=DjangoJSONEncoder),
            )
            logger.error(json.dumps(message))
            time.sleep(count_send_sms_code * 2)

    return sms_result
