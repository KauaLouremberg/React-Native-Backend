import traceback

from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_201_CREATED
from rest_framework.views import APIView

from autenticacao.models import Usuario
from websocket.consumers import _send_websocket
from rest_framework import generics
from .models import AreaSegura
from .serializers import AreaSeguraSerializer
from amparado.models import Amparado
from utils import get_responsavel_from_user, enviar_notificacao_responsavel

from rest_framework import viewsets
from .models import Marcadores
from .serializers import MarcadoresSerializer


def dentro_do_raio(lat1, lon1, lat2, lon2, raio_metros):
    from math import radians, sin, cos, sqrt, atan2

    R = 6371000

    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)

    a = sin(dlat / 2) ** 2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    distancia = R * c

    return distancia <= raio_metros

class LocalizacaoView(APIView):

    def get(self):

        print('chegou aqui')
        return Response({"Sucesso!": "Deu certo"})

    def post(self, request):
        usuario = Usuario.objects.get(user_id=request.user.id)

        if usuario.is_amparado:
            try:
                amparado = Amparado.objects.get(usuario_id=usuario.id)
                responsavel = amparado.responsavel

                if not responsavel:
                    return Response({'Erro!': 'Amparado sem Responsavel, Vincule um primeiro!'})

                data = request.data
                latitude = data.get('latitude')
                longitude = data.get('longitude')
                timestamp = timezone.now().isoformat()

                _send_websocket('recebe_localizacao', responsavel.id, {
                    'responsavel_id': responsavel.id,
                    'latitude': latitude,
                    'longitude': longitude,
                    'timestamp': timestamp
                })
            except:
                return Response({'Erro!': 'Amparado nao encontrado!'})

        else:
            return Response({"Retorno": "Usuario Responsavel!"})

        return Response({"Sucesso!": request.data})

class AreaSeguraListCreateView(generics.ListCreateAPIView):
    serializer_class = AreaSeguraSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        responsavel = get_responsavel_from_user(self.request.user)
        return AreaSegura.objects.filter(responsavel_area=responsavel)

    def perform_create(self, serializer):
        responsavel = get_responsavel_from_user(self.request.user)
        usuario = Usuario.objects.get(user=self.request.user)
        if usuario.is_amparado:
            return Response({"Erro!": "Usuario amparado, nao pode criar uma area!"}, status=HTTP_400_BAD_REQUEST)

        serializer.save(responsavel_area=responsavel)

        return Response({"Successo!": "Area criada com sucesso!"}, status=HTTP_201_CREATED)

class LocalizacaoAmparadoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            user = request.user

            try:
                amparado = Amparado.objects.get(usuario__user=user)
            except Amparado.DoesNotExist:
                print("[ERRO] Usuário tentou enviar localização mas não é amparado!")
                return Response({"detail": "Somente amparados enviam localização."}, status=403)

            responsavel = amparado.responsavel

            lat = float(request.data.get("latitude"))
            lon = float(request.data.get("longitude"))

            areas = AreaSegura.objects.filter(responsavel_area=responsavel)

            for area in areas:

                dentro = dentro_do_raio(
                    lat1=area.latitude,
                    lon1=area.longitude,
                    lat2=lat,
                    lon2=lon,
                    raio_metros=area.raio
                )

                if not dentro:
                    enviar_notificacao_responsavel(
                        responsavel,
                        mensagem=f"O amparado {amparado.usuario.nome} saiu da área '{area.nome}'.",
                        area_id=area.id
                    )

            return Response({"status": "ok"})

        except Exception as e:
            print(e)
            traceback.print_exc()
            return Response({"detail": "Erro interno"}, status=500)

class MarcadoresView(generics.ListCreateAPIView):
    serializer_class = MarcadoresSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        usuario = Usuario.objects.get(user=self.request.user)

        if usuario.is_amparado:
            amparado = Amparado.objects.get(usuario=usuario)

        else:
            responsavel = get_responsavel_from_user(self.request.user)
            amparado = responsavel.amparado

            if not amparado:
                raise PermissionError("Responsável não possui amparado vinculado.")

        return Marcadores.objects.filter(amparado_markers=amparado)

    def perform_create(self, serializer):
        usuario = Usuario.objects.get(user=self.request.user)

        if not usuario.is_amparado:
            return Response({"Erro!": "Usuario Responsavel, nao pode criar um marker!"}, status=HTTP_400_BAD_REQUEST)

        try:
            amparado = Amparado.objects.get(usuario=usuario)
        except:
            raise PermissionError("Usuário não possui conta Amparado.")

        serializer.save(amparado_markers=amparado)

        return Response({"Successo!": "Marcador criado com sucesso!"}, status=HTTP_201_CREATED)

class MarcadorDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = MarcadoresSerializer
    permission_classes = [IsAuthenticated]
    lookup_url_kwarg = "id"

    def get_queryset(self):
        usuario = Usuario.objects.get(user=self.request.user)

        if usuario.is_amparado:
            amparado = Amparado.objects.get(usuario=usuario)
        else:
            responsavel = get_responsavel_from_user(self.request.user)
            amparado = responsavel.amparado
            if not amparado:
                raise PermissionError("Responsável não possui amparado vinculado.")

        return Marcadores.objects.filter(amparado_markers=amparado)

    def perform_update(self, serializer):
        usuario = Usuario.objects.get(user=self.request.user)

        if not usuario.is_amparado:
            raise PermissionError("Responsável não pode editar markers.")

        return super().perform_update(serializer)

    def perform_destroy(self, instance):
        usuario = Usuario.objects.get(user=self.request.user)

        if not usuario.is_amparado:
            raise PermissionError("Responsável não pode deletar markers.")

        return super().perform_destroy(instance)





