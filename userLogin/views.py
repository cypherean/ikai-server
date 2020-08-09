from django.conf import settings
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from rest_framework.response import Response
import json
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required


@api_view(['POST'])
def signup(request):
    body = json.loads(request.body)
    try:
        user_data = {
            'username': body['username'],
            'first_name': body['first_name'],
            'last_name': body['last_name'],
            'email': body['email'],
            'password': body['password'],
        }
    except KeyError as err:
        return Response({
            'status': 'error',
            'message': f'Invalid data provided: {err}'
        }, status=400)
    try:
        new_user = User(**user_data)
        new_user.save()
    except Exception as err:
        return Response({
            'status': 'error',
            'message': f'Could not add new user: {err}'
        }, status=400)
    return Response({
        'status': 'success',
        'message': f'User: {new_user.username} was successfully added',
    })


@api_view(['POST'])
def loginUser(request):
    body = json.loads(request.body)
    try:
        username = body['username']
        password = body['password']
    except KeyError as e:
        return Response({
            'status': 'error',
            'message': f'Invalid data provided: {err}'
        }, status=400)
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return Response({
            'status': 'success',
            'message': f'User: {username} logged in',
        })
    return Response({
        'status': 'error',
        'message': 'Invalid Credentials',
    }, status=400)


@api_view(['GET'])
def logoutUser(request):
    if request.user.is_anonymous:
        return Response({
            'status': 'error',
            'message': f'no user is logged in'
        }, status=400)
    try:
        logout(request)
    except Exception as err:
        return Response({
            'status': 'error',
            'message': f'Error while logging out: {err}'
        }, status=400)
    return Response({
        'status': 'success',
        'message': 'user successfully logged out'
    })


@api_view(['GET'])
def hello(request):
    return Response({
        'message': f'hello {request.user}'
    })
