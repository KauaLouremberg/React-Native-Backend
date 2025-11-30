import uuid

from rest_framework.permissions import IsAuthenticated
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_200_OK
from rest_framework.views import APIView
from rest_framework.response import Response

from amparado.models import Amparado
from autenticacao.models import Usuario
from autenticacao.serializers import UserCreateSerializer

class AmparadoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self):
        return Response({"msg": "GET OK"})

    def post(self, request):
        data = request.data
        serializer = UserCreateSerializer(data=data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            usuario = Usuario.objects.create(
                user=user,
                nome=user.username,
                is_amparado=True
            )

            Amparado.objects.create(
                usuario=usuario,
            )

            return Response({"Sucesso!": "Amparado Criado com Sucesso!"})

        return Response({"Error!": "Algo deu Errado!"})

class AmparadoCodigoView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if self.request.query_params.get('code'):
            amparado = Amparado.objects.get(usuario__user__id=request.user.id)
            codigo = amparado.codigo_convite

            if not codigo:
                return Response({"Erro!": "Amparado nao tem codigo gerado!"}, status=HTTP_400_BAD_REQUEST)
            return Response(codigo, status=HTTP_200_OK)

        id = str(uuid.uuid4())[:8].upper()

        amparado = Amparado.objects.get(usuario__user__id=request.user.id)
        amparado.codigo_convite = id
        amparado.save()

        return Response(id)






