import random

from django.conf import settings


def generate_code(send_sms_code: bool) -> int:
    if send_sms_code is False:
        return settings.SMS_TEST_SMS_CODE
    return random.randint(100000, 999999)
