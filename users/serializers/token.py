from django.contrib.auth import authenticate
from rest_framework import serializers
from users.models import User
from rest_framework.exceptions import AuthenticationFailed


class LoginTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=60, min_length=3)
    password = serializers.CharField(max_length=60, min_length=6, write_only=True)
    tokens = serializers.CharField(min_length=6, read_only=True)

    def validate(self, validated_data):
        username = validated_data.get('username', '')
        password = validated_data.get('password', '')

        user = authenticate(username=username, password=password)

        if not user:
            raise AuthenticationFailed('Invalid credentials. try again')

        if user.is_suspended:
            raise AuthenticationFailed('Account suspended, contact admin')

        return {
            'username': user.username,
            'tokens': user.tokens()
        }

    class Meta:
        model = User
        fields = ('username', 'password', 'tokens',)
