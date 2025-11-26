from django.utils import timezone

from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView

from amparado.models import Amparado
from autenticacao.models import Usuario
from perfil.models import Perfil, Responsavel
from websocket.consumers import _send_websocket


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

