from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from amparado.models import Amparado
from autenticacao.models import Usuario
from firebase.fcm import send_push
from notifications.models import Device
from perfil.models import Perfil, Responsavel
from websocket.consumers import _send_websocket
from rest_framework import generics, permissions
from .models import AreaSegura
from .serializers import AreaSeguraSerializer
from perfil.models import Responsavel
from amparado.models import Amparado
from utils import get_responsavel_from_user, enviar_notificacao_responsavel


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
        serializer.save(responsavel_area=responsavel)


class LocalizacaoAmparadoView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user

        try:
            amparado = Amparado.objects.get(usuario__user=user)
        except Amparado.DoesNotExist:
            return Response({"detail": "Somente amparados enviam localização."}, status=403)

        responsavel = amparado.responsavel

        lat = float(request.data["latitude"])
        lon = float(request.data["longitude"])

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




