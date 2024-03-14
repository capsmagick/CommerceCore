from rest_framework import status
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSignupModelSerializer
from users.serializers import LoginSerializer
from users.serializers import ResetPassword

from .utils import get_userdata


class Signup(APIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSignupModelSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            'message': 'Successfully Signed up..!',
            'data': serializer.data
        }, status=status.HTTP_201_CREATED)


class Login(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = LoginSerializer(data=request.data, **{'request': request})

        if serializer.is_valid(raise_exception=True):
            user = serializer.login(self.request)

            return Response({
                'user': get_userdata(user),
                'message': 'Successfully logined'
            }, status=status.HTTP_200_OK)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        logout(request)
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = ResetPassword(data=request.data, **{'request': request})

        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data['confirm_password']
            serializer.save(password)

            return Response({
                'success': True,
                'message': 'Successfully Password Updated'
            }, status=status.HTTP_200_OK)

