from django.db import models
from userLogin.models import MyUser
from django.utils.timezone import now
ROOM_TYPE_CHOICES = (
    ('GROUP', 'GROUP'),
    ('PERSONAL', 'PERSONAL')
)
STATUS_CHOICES = (('PENDING', 'PENDING'), ('ACCEPTED',
                                           'ACCEPTED'))


class ChatRoom(models.Model):
    name = models.CharField(max_length=50)
    room_type = models.CharField(max_length=20, choices=ROOM_TYPE_CHOICES)
    created_at = models.DateTimeField(default=now, null=True)
    updated_at = models.DateTimeField(default=now, null=True, blank=True)
    last_message = models.CharField(max_length=50, blank=True, null=True)
    verified = models.BooleanField(default=False)


class Message(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
    author = models.ForeignKey(MyUser, on_delete=models.PROTECT)
    content = models.CharField(max_length=2000)
    timestamp = models.DateTimeField(default=now, null=True)


class ChatRoomPermission(models.Model):
    chatroom = models.ForeignKey(ChatRoom, on_delete=models.PROTECT)
    user = models.ForeignKey(MyUser, on_delete=models.PROTECT)

    @property
    def name(self):
        return self.chatroom.name


class Requests(models.Model):
    sender = models.ForeignKey(
        MyUser, on_delete=models.PROTECT, related_name='%(class)s_sender')
    receiver = models.ForeignKey(
        MyUser, on_delete=models.PROTECT, related_name='%(class)s_receiver')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    chatroom = models.OneToOneField(
        ChatRoom, on_delete=models.PROTECT, null=True)
