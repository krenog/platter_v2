from django.conf.urls import include
from django.urls import path

from users import views

api_v1__auth_urls = [
    path(
        'send-sms-code/',
        views.SendSmsView.as_view(),
        name='send_sms_code_view'
    ),
    path(
        'sing-in/',
        views.SingInView.as_view(),
        name='sing_in_view'
    ),
    path(
        'check/',
        views.CheckView.as_view(),
        name='check'
    ),
]

urlpatterns = [
    path('v1/auth/', include(api_v1__auth_urls)),
]
