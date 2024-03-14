from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from django.views.decorators.csrf import ensure_csrf_cookie
from django.utils.decorators import method_decorator
from django.middleware.csrf import get_token

from .utils import get_userdata


# @method_decorator(ensure_csrf_cookie, name='dispatch')
class Me(APIView):
    def get(self, request):

        user = request.user

        if user.is_authenticated:
            response = Response({
                'loggedIn': True,
                'user': get_userdata(user)
            }, status=status.HTTP_200_OK)
            return response

        else:
            return Response({
                'loggedIn': False,
            }, status=status.HTTP_200_OK)

