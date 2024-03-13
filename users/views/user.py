from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from .utils import get_userdata


class Me(APIView):
    def get(self, request):

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

