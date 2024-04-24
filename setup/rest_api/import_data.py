import openpyxl

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.conf import settings
from django.apps import apps
from setup.serializer import ImportSerializer


class ImportTableData(APIView):

    def post(self, request):
        serializer = ImportSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        model_name = serializer.validated_data.get('model')
        file = serializer.validated_data.get('import_file')

        model_class = None

        for model in apps.get_models():
            if model_name == model.__name__:
                model_class = model
                break

        print('===================================')
        print('model: ', model_class.objects.all().count())
        print('File: ', file)
        print('===================================')


        wb = openpyxl.load_workbook(file)
        sheet = wb.active

        for row in sheet.iter_rows(values_only=True, min_row=2):
            print('--------------------------------------------')
            print('row : ', row)
            print('--------------------------------------------')

        return Response({
            'message': 'Success'
        }, status=status.HTTP_200_OK)


