import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
from django.contrib.auth.models import User
from datetime import datetime
from django.utils import timezone
from rest_framework.authtoken.models import Token


class ChatConsumer(WebsocketConsumer):
    def connect(self):
        try:
            self.chatroom_id = self.scope['url_route']['kwargs']['room_id']
            self.chatroom_group_id = 'chat_%s' % self.chatroom_id
        except KeyError as err:
            print(f"Invalid request to connect to websocket: {err}")
            return
        async_to_sync(self.channel_layer.group_add)(
            self.chatroom_group_id,
            self.channel_name
        )
        self.accept()
        self.user = None
        print("connection accepted.")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # django channel authentication:
        if self.user:
            pass
        else:
            try:
                data = json.loads(text_data)
                if 'token' in data.keys():
                    token = data['token']
                    user = Token.objects.get(key=token).user
                    self.user = user
                    print(f"User: {user.username} is now authenticated")
            except Exception as e:
                print(e)
                pass
        if not self.user:
            self.send(json.dumps({'err': 'unauthorized'}))
            self.close()
            return
        text_data = json.loads(text_data)
        print(text_data)
        if text_data['command'] == 'new_message':
            self.new_message_handler(text_data)
        elif text_data['command'] == 'fetch_messages':
            self.fetch_page_messages(self.chatroom_id)
        elif text_data['command'] == 'fetch_prev_messages':
            self.fetch_prev_messages(self.chatroom_id, text_data['time'])
        elif text_data['command'] == 'last':
            self.fetch_prev_message(self.chatroom_id)
        elif text_data['command'] == 'ping':
            pass

    def chat_message(self, event):
        self.send(json.dumps({'typ': 'refresh'}))

    def save_message(self, text_data):
        chatroom = ChatRoom.objects.filter(id=self.chatroom_id)
        other_user = User.objects.get(username=text_data['username'])
        message_data = {
            'chatroom': chatroom[0],
            'author': self.user,
            'authorized': self.user,
            'content': text_data['message1']
        }
        new_message = Message(**message_data)
        new_message.save()
        message_data = {
            'chatroom': chatroom[0],
            'author': self.user,
            'authorized': other_user,
            'content': text_data['message2']
        }
        new_message = Message(**message_data)
        new_message.save()

    def fetch_prev_message(self, chatroom_id, time):
        message = Message.objects.filter(chatroom_id=chatroom_id, timestamp__lt=timezone.make_aware(datetime.strptime(time, '%Y-%m-%d %H:%M:%S')), authorized=self.user).order_by(
            '-timestamp')[0]
        page_messages = []
        page_messages.append({
            'chatroom': message.chatroom.id,
            'author': message.author.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'typ': 'old'
        })
        self.send(json.dumps(
            {'typ': 'old', 'messages': page_messages}))

    def fetch_prev_message(self, chatroom_id):
        message = Message.objects.filter(chatroom_id=chatroom_id, authorized=self.user).order_by(
            '-timestamp')[0]
        page_messages = []
        page_messages.append({
            'chatroom': message.chatroom.id,
            'author': message.author.username,
            'content': message.content,
            'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
            'typ': 'new'
        })
        self.send(json.dumps(
            {'typ': 'new', 'messages': page_messages}))

    def fetch_page_messages(self, chatroom_id):
        messages = Message.objects.filter(chatroom_id=chatroom_id, authorized=self.user).order_by(
            '-timestamp')[0:10]
        messages = Reverse(messages)
        page_messages = []
        for message in messages:
            page_messages.append({
                'chatroom': message.chatroom.id,
                'author': message.author.username,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'typ': 'new'
            })
        self.send(json.dumps(
            {'typ': 'new', 'messages': page_messages}))

    def new_message_handler(self, text_data):
        self.save_message(text_data)
        async_to_sync(self.channel_layer.group_send)(
            self.chatroom_group_id,
            {
                'type': 'chat_message',
            }
        )


def Reverse(lst):
    return [ele for ele in reversed(lst)]
