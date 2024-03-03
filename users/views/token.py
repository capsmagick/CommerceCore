from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import AllowAny

from users.serializers import LoginTokenSerializer


class TokenLoginAPTView(GenericAPIView):
    permission_classes = (AllowAny,)
    serializer_class = LoginTokenSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)