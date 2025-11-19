from django.urls import path
from .views import RegisterDevice, SendNotification

urlpatterns = [
    path("register/", RegisterDevice.as_view(), name='register-device'),
    path("send/", SendNotification.as_view(), name='send-notification'),
]