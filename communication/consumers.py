import json
from channels.generic.websocket import WebsocketConsumer
from asgiref.sync import async_to_sync
from .models import Message
from .serializers import MessageSerializer
from rest_framework.renderers import JSONRenderer

class ChatConsumer(WebsocketConsumer):
    def connect(self):
        self.room_name = "global_chat"
        self.room_group_name = "chat_%s" % self.room_name

        async_to_sync(self.channel_layer.group_add)(
            self.room_group_name,
            self.channel_name
        )

        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.room_group_name,
            self.channel_name
        )

    def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']

        # Сохранение сообщения в базу данных
        author = self.scope['user'] if self.scope['user'].is_authenticated else None
        new_message = Message.objects.create(author=author, content=message)

        # Сериализация нового сообщения
        serializer = MessageSerializer(new_message)
        message_json = JSONRenderer().render(serializer.data).decode('utf-8')

        # Отправка сообщения в группу
        async_to_sync(self.channel_layer.group_send)(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message_json
            }
        )

    def chat_message(self, event):
        message = event['message']

        # Отправка сообщения на WebSocket
        self.send(text_data=json.dumps({
            'message': message
        }))

