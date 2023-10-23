import json

from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from . models import User, GroupChat, Message


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = f"chat_{self.room_name}"

        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()
        
        previous_messages = await self.load_previous_messages()
        for message_content, username in previous_messages:
            await self.send(text_data=json.dumps({
                "message": message_content,
                "username": username
            }))

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = text_data_json['username']
        print(username)
        # DB에 메시지 저장
        await self.save_message(username, message)
        # Send message to room group
        await self.channel_layer.group_send(
            self.room_group_name, {"type": "chat.message", "message": message}
        )

    @database_sync_to_async
    def save_message(self, username, message):
        print(username)
        user = User.objects.get(username=username)
        print(user)
        chat_room = GroupChat.objects.get(room_name=self.room_name)
        chat_room.last_message = message
        chat_room.last_message_sender = user
        
        Message.objects.create(
            group_chat = chat_room,
            sender = user,
            content = message,
        )
    @database_sync_to_async
    def load_previous_messages(self):
        chat_room = GroupChat.objects.get(room_name=self.room_name)
        messages = chat_room.chat_messages.all()
        return [(message.content, message.sender.username) for message in messages]   
        
        
        
    # Receive message from room group
    async def chat_message(self, event):
        message = event["message"]
        username = event['username']

        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message,
                                              "username":username
                                              }))