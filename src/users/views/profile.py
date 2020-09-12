from django.utils.decorators import method_decorator
from rest_framework.generics import GenericAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK

from decorators.validators import validate_request
from users.schemas.profile import ProfileSchema
from users.services.profile import update_profile


class UpdateProfile(GenericAPIView):

    @staticmethod
    def get(request, *args, **kwargs):
        return Response(data=ProfileSchema().dump(request.user), status=HTTP_200_OK)

    @method_decorator(validate_request(schema=ProfileSchema))
    def post(self, request):
        body = request.VALIDATED_DATA
        update_profile(request.user, body)
        return Response(status=HTTP_200_OK)
