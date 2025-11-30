from firebase.fcm import send_push
from notifications.models import Device
from perfil.models import Responsavel
from amparado.models import Amparado
import traceback

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
    print("\n========== ENVIAR NOTIFICAÇÃO RESPONSÁVEL ==========")

    try:
        print(f"[1] Responsável recebido: {responsavel} (id={responsavel.id})")

        # 1 - Obter o Usuario associado ao Responsavel
        usuario = getattr(responsavel, "usuario", None)
        print(f"[2] Usuario encontrado? {bool(usuario)}")

        if usuario is None:
            print("[ERRO] Responsável sem 'usuario' associado!")
            return

        print(f"[2.1] Usuario id={usuario.id}")

        # 2 - Buscar Device
        devices = Device.objects.filter(user_device=usuario)
        print(f"[3] Devices encontrados: {devices.count()}")

        if not devices.exists():
            print("[ERRO] Nenhum device encontrado para este usuário!")
            return

        for device in devices:
            print(f"[3.1] Device encontrado: id={device.id}, token={device.fcm_token[:20]}...")

            token = getattr(device, "fcm_token", None)

            if not token:
                print("[ERRO] Device sem token FCM!")
                continue

            print("[4] Enviando notificação via send_push...")

            try:
                resposta = send_push(
                    token=token,
                    title="Alerta de Área Segura",
                    body=mensagem,
                    data={
                        "tipo": "alerta_area",
                        "area_id": str(area_id) if area_id else "",
                    }
                )
                print(f"[4.1] Resultado do send_push: {resposta}")

            except Exception as e:
                print("[ERRO SEND_PUSH]", e)
                traceback.print_exc()

    except Exception as e:
        print("\n=== ERRO GERAL EM enviar_notificacao_responsavel ===")
        print(e)
        traceback.print_exc()

    print("========== FIM ENVIAR NOTIFICAÇÃO ==========\n")

