from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from amparado.models import Amparado
from autenticacao.models import Usuario
from .models import Perfil, Responsavel
from .serializers import PerfilSerializer, ResponsavelSerializer


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

class ResponsavelViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        print('teste')

    def post(self, request):
        user = Usuario.objects.get(user=request.user)
        data = request.data

        id = data.get("id")

        try:
            amparado = Amparado.objects.get(codigo_convite=id)

            if Responsavel.objects.filter(amparado=amparado).exists():
                return Response({"error": "Esse amparado já está vinculado a outro responsável."},
                                status=status.HTTP_400_BAD_REQUEST)

            responsavel = Responsavel.objects.get(perfil__usuario__user=user)

            responsavel.amparado = amparado
            responsavel.save()

            return Response({"success": "Relacao criada com sucesso!"}, status=status.HTTP_200_OK)

        except:
            return Response({"error": "Nao existe nenhum usuario com esse codigo!"})