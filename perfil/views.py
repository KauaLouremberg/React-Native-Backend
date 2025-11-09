from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from autenticacao.models import Usuario
from .models import Perfil
from .serializers import PerfilSerializer


class PerfilViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Usuario.objects.get(user=request.user)
        perfil, _ = Perfil.objects.get_or_create(usuario=user)
        serializer = PerfilSerializer(perfil)
        return Response(serializer.data)

    def post(self, request):
        user = Usuario.objects.get(user=request.user)

        payload = request.data.get('payload', request.data)
        data = payload.get('params', payload)

        perfil, _ = Perfil.objects.get_or_create(usuario=user)

        serializer = PerfilSerializer(perfil, data=data, partial=True)
        if serializer.is_valid():
            serializer.save(usuario=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnderecoViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        print('teste')