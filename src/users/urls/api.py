from django.conf.urls import include
from django.urls import path

from users import views

api_v1__auth_urls = [
    path(
        'auth/send-sms-code/',
        views.SendSmsView.as_view(),
        name='send_sms_code_view'
    ),
    path(
        'auth/sing-in/',
        views.SingInView.as_view(),
        name='sing_in_view'
    ),
    path(
        'auth/refresh-token/',
        views.RefreshToken.as_view(),
        name='refresh_token_view'
    ),
    path(
        'profile/',
        views.UpdateProfile.as_view(),
        name='profile_view'
    ),
]

urlpatterns = [
    path('v1/user/', include(api_v1__auth_urls)),
]
