from django.urls import path
from .views import PerfilViewSet, EnderecoViewSet

urlpatterns = [
    path('perfil/', PerfilViewSet.as_view(), name='perfil'),
    path('endereco/', EnderecoViewSet.as_view(), name='endereco'),
]