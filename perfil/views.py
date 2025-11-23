from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from amparado.models import Amparado
from autenticacao.models import Usuario
from .models import Perfil, Responsavel, Endereco
from .serializers import PerfilSerializer, ResponsavelSerializer, EnderecoSerializer


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

        if not user.is_amparado:
            try:
                Responsavel.objects.get(perfil=perfil)
            except:
                Responsavel.objects.create(perfil=perfil)

        serializer = PerfilSerializer(perfil, data=data, partial=True)
        if serializer.is_valid():
            serializer.save(usuario=user)
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EnderecoViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = Usuario.objects.get(user=request.user)
        perfil = Perfil.objects.get(usuario=user)
        endereco, _ = Endereco.objects.get_or_create(perfil=perfil)
        serializer = EnderecoSerializer(endereco)
        return Response(serializer.data)

    def post(self, request):
        user = Usuario.objects.get(user=request.user)
        perfil = Perfil.objects.get(usuario=user)

        data = request.data
        endereco, _ = Endereco.objects.get_or_create(perfil=perfil)

        serializer = EnderecoSerializer(endereco, perfil=perfil, data=data)

        if serializer.is_valid():
            serializer.save(usuario=user)

            return Response({"Sucesso!": "Valores salvos com sucesso!"})
        return Response({"Erro!": "Algo deu errado!"})

class ResponsavelViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = Usuario.objects.get(user=request.user)
        data = request.data

        id = data.get("id")

        try:
            amparado = Amparado.objects.get(codigo_convite=id)

            if Responsavel.objects.filter(amparado=amparado).exists():
                return Response({"error": "Esse amparado já está vinculado a outro responsável."},
                                status=status.HTTP_400_BAD_REQUEST)

            responsavel = Responsavel.objects.get(perfil__usuario=user)

            responsavel.amparado = amparado
            responsavel.save()

            amparado.responsavel = responsavel
            amparado.save()

            return Response({"success": "Relacao criada com sucesso!"}, status=status.HTTP_200_OK)

        except:
            return Response({"error": "Nao existe nenhum usuario com esse codigo!"})