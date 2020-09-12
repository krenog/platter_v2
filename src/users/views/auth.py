from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from decorators.validators import validate_request
from users.schemas.auth import SendSMSCodeSchema, SignInSchema, UserSchema, RefreshTokenSchema, NewTokenSchema
from users.services.auth import generate_and_send_code, sign_in, generate_new_token


class SendSmsView(GenericAPIView):
    permission_classes = [AllowAny]

    @method_decorator(validate_request(schema=SendSMSCodeSchema))
    def post(self, request):
        body = request.VALIDATED_DATA
        generate_and_send_code(body['phone_number'])
        return Response(status=HTTP_200_OK)


class SingInView(GenericAPIView):
    permission_classes = [AllowAny]

    @method_decorator(validate_request(schema=SignInSchema))
    def post(self, request):
        body = request.VALIDATED_DATA
        data = sign_in(body['phone_number'], body['code'])
        return Response(data=UserSchema().dump(data), status=HTTP_200_OK)


class RefreshToken(GenericAPIView):
    permission_classes = [AllowAny]

    @method_decorator(validate_request(schema=RefreshTokenSchema))
    def post(self, request):
        body = request.VALIDATED_DATA
        data = generate_new_token(body['refresh_token'])
        return Response(data=NewTokenSchema().dump(data), status=HTTP_200_OK)
