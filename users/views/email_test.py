from rest_framework.views import APIView
from rest_framework.response import Response
from django.conf import settings
from django.core.mail import send_mail


class TestMail(APIView):

    def post(self, request, *args, **kwargs):

        subject = 'Test Mail'
        message = 'This is test mail'
        email_from = settings.EMAIL_HOST_USER
        email = ['rmuwork51@gmail.com']

        send_mail(subject, message, email_from, email)

        return Response('Success')



