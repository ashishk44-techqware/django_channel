from channels.generic.websocket import AsyncWebsocketConsumer
from django.contrib.auth.models import User
from chat.models import *
from channels.db import database_sync_to_async
import json
from datetime import datetime
from django.db.models import Q


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope['url_route']['kwargs']['room_name']
        self.room_group_name = 'chat-%s' % self.room_name
        print(self.room_name,"room")
        print(self.room_group_name,"room1")
        if(self.scope['user'].is_authenticated):
            await self.channel_layer.group_add(
                self.room_group_name,
                self.channel_name
            )
            await self.accept()
            print("hi")
        else:
            await self.close()
            print("close")

    async def disconnect(self, code):
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    @database_sync_to_async
    def save_message(self,message, sender, receiver):
        sender_user = User.objects.get(id=sender)
        receiver_user = User.objects.get(id=receiver)
        room = ChatRoom.objects.filter(Q(sender=sender,receiver=receiver)|Q(sender=receiver,receiver=sender)).first()
        Message.objects.create(message=message, sender=sender_user, receiver=receiver_user,room=room)

    async def receive(self, text_data=None, bytes_data=None):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        sender = str(self.scope['user'].id)
        receiver = text_data_json['receiver']
        await self.save_message(message, sender, receiver)
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                'type': 'chat_message',
                'message': message,
                'sender': sender,
                'receiver': receiver,
                'doc': datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")
            }
        )

    async def chat_message(self, event):
        message = event['message']
        sender = event['sender']
        receiver = event['receiver']
        doc = event['doc']
        await self.send(text_data=json.dumps({
            'message': message,
            'sender': sender,
            'receiver': receiver,
            'doc': doc
        }))
