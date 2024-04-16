from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.serializers import LoginTokenSerializer
from .utils import get_userdata


class TokenLoginAPTView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginTokenSerializer

    def post(self, request):
        """
            Login API Token

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.
            Data:
                username (char): Username of the user.
                password (char): Password of the user.

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LoginStatus(APIView):
    permission_classes = (AllowAny,)
    authentication_classes = (JWTAuthentication,)

    def get(self, request, *args, **kwargs):
        """
            User Status API

            Parameters:
                request (HttpRequest): The HTTP request object containing model data.

            Returns:
                Response: A DRF Response object indicating success or failure and a message.
        """
        user = request.user

        if user.is_authenticated:
            return Response({
                'loggedIn': True,
                'user': get_userdata(user)
            }, status=status.HTTP_200_OK)

        else:
            return Response({
                'loggedIn': False,
            }, status=status.HTTP_200_OK)

