import time

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404

from autenticacao.models import Usuario
from perfil.models import Responsavel
from .models import Device
from firebase.fcm import send_push
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterDevice(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        usuario = Usuario.objects.get(user=request.user)

        token = request.data.get("fcm_token")
        if not token:
            return Response({"error": "fcm_token é obrigatório"}, status=400)

        device, created = Device.objects.update_or_create(
            fcm_token=token,
            defaults={"user_device": usuario}
        )


        return Response({"status": "registered"})



class SendNotification(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        target_id = request.data.get("target_user_id")
        responsavel = get_object_or_404(Responsavel, id=target_id)

        if not hasattr(responsavel, "perfil"):
            return Response({"error": "Responsável sem perfil"}, status=400)

        usuario = responsavel.perfil.usuario
        usuario_alvo = get_object_or_404(Usuario, id=usuario.id)
        devices = Device.objects.filter(user_device=usuario_alvo)

        if not devices.exists():
            return Response({"error": "Nenhum device registrado"}, status=400)

        time.sleep(2)

        for d in devices:
            send_push(
                d.fcm_token,
                "SOS",
                "O botão de SOS foi disparado pelo amparado!"
            )

        return Response({"status": "sent"})