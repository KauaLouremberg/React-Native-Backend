from django.urls import path
from .views import PerfilViewSet, EnderecoViewSet, ResponsavelViewSet

urlpatterns = [
    path('perfil/', PerfilViewSet.as_view(), name='perfil'),
    path('endereco/', EnderecoViewSet.as_view(), name='endereco'),
    path('responsavel/', ResponsavelViewSet.as_view(), name='responsavel'),
]