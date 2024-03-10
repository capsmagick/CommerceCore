from django.contrib.auth import authenticate, login
from rest_framework import serializers
from users.models import User
from users.models.other import AddressRegister


class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(required=True)
    password = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(LoginSerializer, self).__init__(*args, **kwargs)

    def validate(self, validated_data):
        username = validated_data['username']
        password = validated_data['password']

        user = authenticate(self.request, username=username, password=password)

        if not user:
            raise serializers.ValidationError('Invalid credentials')

        self.user = user # noqa

        return validated_data

    def login(self, request):
        if hasattr(self, 'user'):
            login(request, self.user)
            return self.user


class ResetPassword(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    confirm_password = serializers.CharField(required=True)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(ResetPassword, self).__init__(*args, **kwargs)

    def clean(self, attrs):
        username = self.request.user.username
        old_password = attrs.get('old_password')
        new_password = attrs.get('new_password')
        confirm_password = attrs.get('confirm_password')


        user = authenticate(self.request, username=username, password=old_password)

        if not user:
            raise serializers.ValidationError(
                {
                    'old_password': 'Invalid password'
                }
            )

        if new_password != confirm_password:
            raise serializers.ValidationError(
                {
                    'new_password': "Password doesn't match"
                }
            )

        self.user = user # noqa

        return attrs

    def save(self, password):
        self.user.set_password(password)
        self.user.save()


class AddressRegisterModelSerializer(serializers.ModelSerializer):
    def clean(self, attrs):
        pass

    class Meta:
        model = AddressRegister
        fields = '__all__'


