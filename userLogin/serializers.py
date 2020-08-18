from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from userLogin.models import UserKeys
from django.contrib.auth.models import User


class CustomRegisterSerializer(RegisterSerializer):

    username = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True)
    publickey = serializers.CharField(required=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()
        return {
            'password': self.validated_data.get('password1', ''),
            'username': self.validated_data.get('username', ''),
            'publickey': self.validated_data.get('publickey'),
        }

    def save(self, request):
        print("i am here doung my job")
        cleaned_data = self.get_cleaned_data()
        new_user = User(username=cleaned_data['username'])
        new_user.set_password(cleaned_data['password'])
        new_user.save()
        user_keys = UserKeys(
            **{'user': new_user, 'publickey': cleaned_data['publickey']})
        user_keys.save()
        return new_user
