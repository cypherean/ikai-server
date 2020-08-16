from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
import json
from userLogin.models import MyUser
from django.contrib.auth.decorators import login_required
from chat.models import *
from rest_framework import permissions
from rest_framework.decorators import permission_classes
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_auth.registration.views import RegisterView


class CustomRegisterView(RegisterView):
    queryset = MyUser.objects.all()


class Chatrooms(APIView):

    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # user = request.user
        user = MyUser.objects.get(username='burnerlee')
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


class UserSearch(APIView):

    # permission_classes = [IsAuthenticated]
    def get(self, request):
        # request_user = request.user
        request_user = MyUser.objects.get(username='burnerlee')
        username = request_user.username
        try:
            query = request.GET['query']
        except KeyError as e:
            return Response({'err': 'get a query with "query" parameter'}, status=400)
        users = MyUser.objects.filter(username__istartswith=query)
        results = []
        for user in users:
            status = "new"
            if user.username == username:
                continue
            requests = Requests.objects.filter(
                sender=user, receiver=request_user)
            chatroom_id = ''
            if len(requests) > 0:
                if requests[0].status == "PENDING":
                    status = "pending"
                elif requests[0].status == "ACCEPTED":
                    status = "accepted"
            requests = Requests.objects.filter(
                sender=request_user, receiver=user)
            if len(requests) > 0:
                if requests[0].status == "PENDING":
                    status = "requested"
                    chatroom_id = request.chatroom.id
                elif requests[0].status == "ACCEPTED":
                    status = "accepted"
            results.append({'username': user.username,
                            'status': status})
        return Response({'users': results})


class Request(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        # sender = request.user
        sender = MyUser.objects.get(username="burnerlee")
        try:
            query = request.GET['user']
        except KeyError as e:
            return Response({'err': 'get a query with user parameter'}, status=400)
        receiver = MyUser.objects.get(username=query)
        if receiver == sender:
            return Response({'err': 'sender and receiver are the same.INVALID REQUEST'}, status=400)
        data = {
            'name': f"{receiver.username}-{sender.username}",
            'room_type': 'PERSONAL',
        }
        new_chatroom = ChatRoom(**data)
        new_chatroom.save()
        data = {
            'sender': sender,
            'receiver': receiver,
            'status': 'PENDING',
            'chatroom': new_chatroom
        }
        new_request = Requests(**data)
        new_request.save()
        data = {
            'chatroom': new_chatroom,
            'user': sender
        }
        chatroom_pm_send = ChatRoomPermission(**data)
        chatroom_pm_send.save()
        return Response({})


class RequestAccept(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            # acceptor = request.user
            acceptor = MyUser.objects.get(username='mahak')
        except Exception as e:
            return Response({'err': e}, status=400)
        try:
            query = request.GET['user']
        except KeyError as e:
            return Response({'err': 'get a query with user parameter'}, status=400)
        try:
            sender = MyUser.objects.get(username=query)
        except Exception as e:
            return Response({'err': f'user with given username does not exist: {e}'}, status=400)
        request = Requests.objects.filter(sender=sender, receiver=acceptor)
        if len(request) == 0:
            return Response({'err': 'invalid request accept sent'}, status=400)
        try:
            new_chatroom = request[0].chatroom
            request.update(status='ACCEPTED')
            new_chatroom.update(verified=True)
            data = {
                'chatroom': new_chatroom,
                'user': acceptor
            }
            chatroom_pm_recv = ChatRoomPermission(**data)
            chatroom_pm_recv.save()
        except Exception as e:
            return Response({'err': e}, status=400)
        return Response({})


class RequestDecline(APIView):
    # permission_classes = [IsAuthenticated]

    def get(self, request):
        # decliner = request.user
        decliner = MyUser.objects.get(username='mahak')
        try:
            query = request.GET['user']
        except KeyError as e:
            return Response({'err': 'get a query with user parameter'}, status=400)
        sender = MyUser.objects.get(username=query)
        request = Requests.objects.filter(
            sender=sender, receiver=decliner).select_related('chatroom')
        if len(request) == 0:
            return Response({'err': 'invalid request accept sent'}, status=400)
        del_chatroom = request[0].chatroom
        chatroom_pms = ChatRoomPermission.objects.filter(chatroom=del_chatroom)
        request.delete()
        chatroom_pms.delete()
        del_chatroom.delete()
        return Response({})


class PendingRequests(APIView):
    # permission_classes = [IsAuthenticated]
    def get(self, request):
        # request_user = request.user
        request_user = MyUser.objects.get(username='mahak')
        results = []
        pending_requests = Requests.objects.filter(
            status="PENDING", receiver=request_user)
        for pending_request in pending_requests:
            results.append({'username': pending_request.sender.username,
                            'chatroom_id': pending_request.chatroom.id})
        return Response({'users': results})
