import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
from django.contrib.auth.models import User
from datetime import datetime


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        try:
            self.chatroom_id = self.scope['url_route']['kwargs']['room_id']
            self.chatroom_group_id = 'chat_%s' % self.chatroom_id
            # self.user = self.scope['user']
        except KeyError as err:
            print(f"Invalid request to connect to websocket: {err}")
            return
        # if self.user.is_anonymous:
        #     print(
        #         f"Anonymous user trying to connect to websocket to Chatroom id:{self.chatroom_id}, disconnecting.")
        #     return
        # user_has_permission = len(ChatRoomPermission.objects.filter(
        #     user=self.user, chatroom_id=self.chatroom_id)) > 0
        # if not user_has_permission:
        #     print(
        #         f"user with username ({self.user}) trying to connect to websocket to unauthorized chatroom id:{self.chatroom_id}, disconnecting.")
        #     return
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_group_id,
            self.channel_name
        )
        self.accept()

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        text_data = json.loads(text_data)
        if text_data['command'] == 'new_message':
            self.new_message_handler(text_data)
        elif text_data['command'] == 'fetch_messages':
            self.fetch_page_messages(self.chatroom_id, int(text_data['page']))

    def chat_message(self, event):
        message_details = event['message_details']
        self.send(json.dumps({'len': 1, 'messages': [message_details]}))

    def save_message(self, text_data):
        chatroom = ChatRoom.objects.get(id=self.chatroom_id)
        author = User.objects.get(username='test')
        message_data = {
            'chatroom': chatroom,
            # author:self.user,
            'author': author,
            'content': text_data['message']
        }
        new_message = Message(**message_data)
        new_message.save()

    def fetch_page_messages(self, chatroom_id, page):
        messages = Message.objects.filter(chatroom_id=chatroom_id).order_by(
            '-timestamp')[(page-1)*10:page*10]
        page_messages = []
        for message in messages:
            page_messages.append({
                'chatroom': message.chatroom.id,
                'author': message.author.username,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S')
            })
        self.send(json.dumps(
            {'len': len(page_messages), 'messages': [page_messages]}))

    def new_message_handler(self, text_data):
        self.save_message(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_group_id,
            {
                'type': 'chat_message',
                'message_details': {
                    'chatroom': self.chatroom_id,
                    # 'author':self.user.username,
                    'author': 'test',
                    'content': text_data['message'],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                }
            }
        )
