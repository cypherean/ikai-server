from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
import json
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from chat.models import *
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class Chatrooms(APIView):

    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        chatrooms = ChatRoomPermission.objects.select_related(
            'chatroom').filter(user=user)
        result = []
        for chatroom in chatrooms:
            result.append(
                {
                    'id': chatroom.chatroom.id,
                    'name': chatroom.chatroom.name,
                    'room_type': chatroom.chatroom.room_type,
                    'updated_at': chatroom.chatroom.updated_at.strftime("%H:%M"),
                    'updated_at_date': chatroom.chatroom.updated_at.strftime("%d/%m"),
                    'last_message': chatroom.chatroom.last_message
                }
            )
        return Response({
            'results': result
        })
