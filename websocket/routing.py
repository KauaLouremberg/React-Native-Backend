from django.urls import path
from . import consumers

websocket_urlpatterns = [
    path('ws/localizacao/<str:usuario_id>/', consumers.LocalizacaoConsumer.as_asgi()),
]

