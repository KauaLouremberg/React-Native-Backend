import json
import logging

from asgiref.sync import async_to_sync
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.layers import get_channel_layer

logger = logging.getLogger(__name__)

def _send_websocket(type, usuario_id, context):
    room_name = f'websocket_{usuario_id}'
    channel_layer = get_channel_layer()
    async_to_sync(channel_layer.group_send)(room_name, {'type': type, 'object': context})

class LocalizacaoConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        try:
            logger.info(f"Iniciando conexao com websocket")
            self.room_name = self.scope['url_route']['kwargs']['usuario_id']
            self.room_group_name = f"websocket_{self.room_name}"

            if not self.channel_layer:
                await self.close()
                return

            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )

            await self.accept()

        except Exception as e:
            logger.info(f"Ocorreu um erro ao conectar ao websocket: {e}")


    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    async def receive(self, text_data):
        logger.info('Recebendo Websocket')

        data = json.loads(text_data)
        type_ = data['type']
        object_ = data['object']

        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': type_,
                'object': object_
            }
        )


    async def recebe_localizacao(self, event):
        await self.send(text_data=json.dumps({
            'type': 'recebe_localizacao',
            'responsavel_id': event['object']['responsavel_id'],
            'latitude': event['object']['latitude'],
            'longitude': event['object']['longitude'],
            'timestamp': event['object']['timestamp'],
        }))