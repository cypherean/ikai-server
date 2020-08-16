import json
from asgiref.sync import async_to_sync
from channels.generic.websocket import WebsocketConsumer
from .models import *
from userLogin.models import MyUser
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
        print("connection accepted.")

    def disconnect(self, close_code):
        async_to_sync(self.channel_layer.group_discard)(
            self.chatroom_group_id,
            self.channel_name
        )

    # Receive message from WebSocket
    def receive(self, text_data):
        # django channel authentication:
        if self.scope['user'].id:
            pass
        else:
            try:
                data = json.loads(text_data)
                if 'token' in data.keys():
                    token = data['token']
                    username = Token.objects.get(key=token)
                    user = MyUser.objects.get(username=username)
                    self.scope['user'] = user
                    print(f"User: {username} is now authenticated")
            except Exception as e:
                print(e)
                pass
        if not self.scope['user'].id:
            self.send(json.dumps({'err': 'unauthorized'}))
            self.close()
            return
        text_data = json.loads(text_data)
        if text_data['command'] == 'new_message':
            self.new_message_handler(text_data)
        elif text_data['command'] == 'fetch_messages':
            self.fetch_page_messages(self.chatroom_id)
        elif text_data['command'] == 'fetch_prev_messages':
            self.fetch_prev_messages(self.chatroom_id, text_data['time'])

    def chat_message(self, event):
        message_details = event['message_details']
        self.send(json.dumps({'typ': 'new', 'messages': [message_details]}))

    def save_message(self, text_data):
        chatroom = ChatRoom.objects.filter(id=self.chatroom_id)
        chatroom.update(updated_at=datetime.now(),
                        last_message=text_data['message'][:50])
        author = MyUser.objects.get(username=text_data['username'])
        message_data = {
            'chatroom': chatroom[0],
            # author:self.user,
            'author': author,
            'content': text_data['message']
        }
        new_message = Message(**message_data)
        new_message.save()

    def fetch_prev_messages(self, chatroom_id, time):
        messages = Message.objects.filter(chatroom_id=chatroom_id, timestamp__lt=timezone.make_aware(datetime.strptime(time, '%Y-%m-%d %H:%M:%S'))).order_by(
            '-timestamp')[0:10]
        messages = Reverse(messages)
        page_messages = []
        for message in messages:
            page_messages.append({
                'chatroom': message.chatroom.id,
                'author': message.author.username,
                'content': message.content,
                'timestamp': message.timestamp.strftime('%Y-%m-%d %H:%M:%S'),
                'typ': 'old'
            })
        self.send(json.dumps(
            {'typ': 'old', 'messages': page_messages}))

    def fetch_page_messages(self, chatroom_id):
        messages = Message.objects.filter(chatroom_id=chatroom_id).order_by(
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
                'message_details': {
                    'chatroom': self.chatroom_id,
                    'author': text_data['username'],
                    'content': text_data['message'],
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                    'typ': 'new'
                }
            }
        )


def Reverse(lst):
    return [ele for ele in reversed(lst)]
