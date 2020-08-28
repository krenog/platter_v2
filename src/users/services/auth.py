from collections import namedtuple

from django.conf import settings
from django.core.cache import cache
from rest_framework_simplejwt.tokens import RefreshToken, Token

from errors.errors import ClientError
from services.sms.api import send_sms
from users.models import verification_code, User

SignInResponseData = namedtuple('SignInResponseData', 'id, phone_number, token, refresh_token')


def generate_and_send_code(phone_number: str) -> None:
    need_sms = settings.SMS_GATEWAY_ENABLED
    if phone_number == str(settings.SMS_TEST_PHONE_NUMBER):
        need_sms = False
    code = verification_code.generate_code(need_sms)
    cache.set(phone_number, code, settings.SMS_CODE_TTL)
    cache.set(f"{phone_number}_count_try_code", 0)
    if need_sms is True:
        send_sms(phone_number=phone_number, text=str(code))


def sign_in(phone_number: str, code: str) -> SignInResponseData:
    validate_code(phone_number, code)
    user = User.objects.get_or_create_user(phone_number=phone_number)
    delete_code_from_cache(phone_number)
    refresh = get_tokens_for_user(user)
    return SignInResponseData(
        id=user.id,
        phone_number=phone_number,
        token=str(refresh.access_token),
        refresh_token=str(refresh)
    )


def validate_code(phone_number: str, code: str) -> None:
    code_from_cache = cache.get(phone_number)
    # валидируем код
    if len(str(code)) != int(settings.LENGTH_SMS_CODE):
        raise ClientError(
            code='code_validation_error',
            detail="Sms code valid error",
        )
    # если кода не существует
    if code_from_cache is None:
        raise ClientError(
            code='code_does_not_exist',
            detail="Sms code valid error",
        )
    compare_code(code_from_cache, code, phone_number)


def compare_code(code_from_cache: str, code: str, phone_number: str) -> None:
    # увеличиваем количество попыток ввода кода
    count_try_code = cache.incr(f"{phone_number}_count_try_code")
    # проверяем количество попыток ввода кода
    if int(count_try_code) >= 5:
        # слишком много запросов
        raise ClientError(
            code='too_many_attempts',
            detail="Sms code valid error",
        )
    # проверяем на совпадение кода из редиса
    if str(code) != str(code_from_cache):
        raise ClientError(
            code='invalid_verification_code',
            detail="Sms code valid error",
        )


def get_tokens_for_user(user: User) -> RefreshToken:
    return RefreshToken.for_user(user)


def delete_code_from_cache(phone_number: str) -> None:
    cache.delete(phone_number)
