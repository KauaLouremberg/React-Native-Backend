from .models import Perfil, Endereco
from .serializers import PerfilSerializer, EnderecoSerializer
from rest_framework import viewsets


class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer


class EnderecoViewSet(viewsets.ModelViewSet):
    queryset = Endereco.objects.all()
    serializer_class = EnderecoSerializer