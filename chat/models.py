from django.db import models
from django.contrib.auth.models import User

ROOM_TYPE_CHOICES = (
    ('GROUP', 'GROUP'),
    ('PERSONAL', 'PERSONAL')
)


class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    created_at = models.TimeField(auto_now_add=True)


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.CharField(max_length=255)
    timestamp = models.TimeField(auto_now_add=True)


class ChatRoomPermission(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
