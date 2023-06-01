import json

from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async

from .models import Room, Message
from django.contrib.auth.models import User

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        print("room name: ", self.room_name)
        # self.room_group_name = f'chat_{self.room_name}'
        # print("room group name: ", self.room_group_name)

        await self.channel_layer.group_add(
            # self.room_group_name,
            self.room_name,
            self.channel_name,
        )

        await self.accept()

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            # self.room_group_name,
            self.room_name,
            self.channel_name,
        )

    async def receive(self, text_data):
        data = json.loads(text_data)
        message = data['message']
        username = data['username']
        room = data['room']

        await self.save_message(username, message, room)

        await self.channel_layer.group_send(
            # self.room_group_name,
            self.room_name,
            {
                'type': 'chat_message',
                'message': message,
                'username': username,
                'room': room,
            }
        )

    async def chat_message(self, event):
        message = event['message']
        username = event['username']
        room = event['room']

        print('Room...', room)

        await self.send(text_data=json.dumps({
            'message': message,
            'username': username,
            'room': room,
        }))

    @sync_to_async
    def save_message(self, username, message, room):
        user = User.objects.get(username=username)
        room = Room.objects.get(id=room)

        Message.objects.create(
            user=user,
            room=room,
            content=message
        )
        