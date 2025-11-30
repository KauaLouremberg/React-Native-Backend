from firebase.fcm import send_push
from notifications.models import Device
from perfil.models import Responsavel
from amparado.models import Amparado

def get_responsavel_from_user(user):
    # Usuário logado é um responsável
    try:
        return Responsavel.objects.get(perfil__usuario__user=user)
    except Responsavel.DoesNotExist:
        pass

    # Usuário logado é um amparado
    try:
        amparado = Amparado.objects.get(usuario__user=user)
        return amparado.responsavel
    except Amparado.DoesNotExist:
        pass

    return None

def enviar_notificacao_responsavel(responsavel, mensagem, area_id=None):
    usuario = responsavel.usuario
    device = Device.objects.get(usuario=usuario)

    token = getattr(device, "fcm_token", None)

    if not token:
        print("Responsável sem token FCM.")
        return

    return send_push(
        token=token,
        title="Alerta de Área Segura",
        body=mensagem,
        data={
            "tipo": "alerta_area",
            "area_id": str(area_id) if area_id else "",
        }
    )
