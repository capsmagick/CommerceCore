from rest_framework import status
from django.contrib.auth import logout
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated

from users.serializers import UserSignupModelSerializer
from users.serializers import LoginSerializer
from users.serializers import ResetPassword

from users.utils import get_userdata


class Signup(APIView):
    """
        API For Signup the customer to our site
    """
    permission_classes = (AllowAny,)
    serializer_class = UserSignupModelSerializer

    def post(self, request, *args, **kwargs):
        """
            POST API to save the details of customer

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
            Data:
                __all__ fields present in the serializer class

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """

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
        """
            Login API Session

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
            Data:
                username (char): Username of the user.
                password (char): Password of the user.

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        serializer = LoginSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.login(self.request)

            return Response({
                'user': get_userdata(user),
                'message': 'Successfully logined'
            }, status=status.HTTP_200_OK)


class Logout(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
            Logout API Session

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        logout(request)
        return Response({
            'message': 'Successfully logged out'
        }, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        """
            Change Password API

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
            Data:
                old_password (char): The old password of the user.
                new_password (char): The new password of the user.
                confirm_password (char): The new password of the user [Retyped].

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        serializer = ResetPassword(data=request.data)

        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data['confirm_password']
            serializer.save(password=password)
            logout(request)
            return Response({
                'success': True,
                'message': 'Successfully Password Updated'
            }, status=status.HTTP_200_OK)

