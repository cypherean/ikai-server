from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chatroom_id', 'author', 'content', 'timestamp')


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'room_type', 'verified',
                    'created_at', 'updated_at')


@admin.register(ChatRoomPermission)
class ChatRoomPermission(admin.ModelAdmin):
    list_display = ('name', 'user')


@admin.register(Requests)
class Requests(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'status')
