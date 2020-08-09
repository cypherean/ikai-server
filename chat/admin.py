from django.contrib import admin
from .models import *
# Register your models here.


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('chatroom_id', 'author', 'content')


@admin.register(ChatRoom)
class ChatRoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'id', 'room_type', 'created_at')


@admin.register(ChatRoomPermission)
class ChatRoomPermission(admin.ModelAdmin):
    list_display = ('chatroom', 'user')
