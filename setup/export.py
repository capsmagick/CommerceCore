from openpyxl import Workbook
from rest_framework.decorators import action
from django.http import HttpResponse
import datetime


class ExportData:
    EXCLUDE_FIELDS = ['deleted', 'deleted_at', 'deleted_by']

    def generate_headers(self, model, include_deleted):
        row = []
        for field in model._meta.fields:
            if include_deleted or field.name not in self.EXCLUDE_FIELDS:
                row.append(field.verbose_name)
        return row

    @action(detail=False, methods=['GET'], url_path='export')
    def generate_excel(self, request, *args, **kwargs):
        include_deleted = request.GET.get('includeDeleted', False)

        queryset = self.filter_queryset(self.get_queryset())
        model = queryset.model

        today = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M")

        file_name = f"{model.__name__}_{today}"

        wb = Workbook()

        ws = wb.active

        headers = self.generate_headers(model, include_deleted)

        ws.append(headers)

        for obj in queryset:
            row = []
            for field in model._meta.fields:
                print('field : ', field.get_internal_type())
                field_type = field.get_internal_type()
                if include_deleted or field.name not in self.EXCLUDE_FIELDS:
                    data = getattr(obj, field.name)
                    print('field.name : ', field.name)
                    print('data.__str__() : ', data.__str__())
                    print('data : ', data)
                    print('type data : ', type(data))
                    if field_type == 'DateTimeField':
                        data = data.strftime("%Y-%m-%d %I:%M %p") if data else ''
                        row.append(data)
                    elif field_type == 'DateField':
                        data = data.strftime("%Y-%m-%d") if data else ''
                        row.append(data)
                    elif field_type == 'ForeignKey':
                        row.append(data.__str__())
                    else:
                        row.append(str(getattr(obj, field.name)))

            ws.append(row)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={file_name}.xlsx'

        # Save the workbook to the response
        wb.save(response)

        return response





