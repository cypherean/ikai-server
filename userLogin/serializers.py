from rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from userLogin.models import MyUser


class CustomRegisterSerializer(RegisterSerializer):

    username = serializers.CharField(required=True)
    password1 = serializers.CharField(write_only=True)
    public_key = serializers.CharField(required=True)

    def get_cleaned_data(self):
        super(CustomRegisterSerializer, self).get_cleaned_data()

        return {
            'password1': self.validated_data.get('password1', ''),
            'username': self.validated_data.get('username', ''),
            'public_key': self.validated_data.get('public_key', ''),
        }


class CustomUserDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = MyUser
        fields = ('username', 'public_key')
        read_only_fields = ('username',)
