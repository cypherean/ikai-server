from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
ROOM_TYPE_CHOICES = (
    ('GROUP', 'GROUP'),
    ('PERSONAL', 'PERSONAL')
)


class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    created_at = models.DateTimeField(default=now, null=True)
    updated_at = models.DateTimeField(null=True, blank=True)
    last_message = models.CharField(max_length=50, blank=True, null=True)


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
    author = models.ForeignKey(User, on_delete=models.PROTECT)
    content = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(default=now, null=True)


class ChatRoomPermission(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
    user = models.ForeignKey(User, on_delete=models.PROTECT)
