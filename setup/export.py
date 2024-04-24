from openpyxl import Workbook
from openpyxl.styles import Font, Border, Side
from rest_framework.decorators import action
from django.http import HttpResponse
import datetime


class ExportData:
    EXCLUDE_FIELDS = ['deleted', 'deleted_at', 'deleted_by']
    EMPTY_VALUES = [None, '', ' ', 'undefined', '[]']

    def generate_headers(self, model, include_deleted):
        headers = []
        for field in model._meta.fields:
            if include_deleted or field.name not in self.EXCLUDE_FIELDS:
                headers.append(field.verbose_name)

        # Include many-to-many field headers
        print('model._meta.related_objects : ', model._meta.many_to_many)
        print('model._meta.related_objects : ', model._meta.related_objects)
        for field in model._meta.many_to_many:
            if field.many_to_many:
                headers.append(field.verbose_name)

        return headers

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
        # Write headers to the worksheet and apply styling
        header_row = ws.append(headers)
        for cell in header_row:
            cell.font = Font(bold=True)  # Make headers bold
            cell.border = Border(bottom=Side(style='thin'))  # Add border to the bottom of header cells

        for obj in queryset:
            row = []
            for field in model._meta.fields:
                field_type = field.get_internal_type()
                if include_deleted or field.name not in self.EXCLUDE_FIELDS:
                    data = getattr(obj, field.name)
                    if field_type == 'DateTimeField':
                        data = data.strftime("%Y-%m-%d %I:%M %p") if data not in self.EMPTY_VALUES else ''
                    elif field_type == 'DateField':
                        data = data.strftime("%Y-%m-%d") if data not in self.EMPTY_VALUES else ''
                    elif field_type == 'ForeignKey':
                        data = str(data) if data not in self.EMPTY_VALUES else ''
                    elif field_type == 'BooleanField':
                        data = 'Yes' if data else 'No'
                    else:
                        data = str(data) if data not in self.EMPTY_VALUES else ''

                    row.append(data)

            # Include many-to-many field data
            for relation in model._meta.many_to_many:
                if relation.many_to_many:
                    related_data = getattr(obj, relation.name).all()
                    data = ', '.join(str(item) for item in related_data) if related_data else ''
                    print('data : ', data)
                    row.append(data)
            ws.append(row)

        response = HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition'] = f'attachment; filename={file_name}.xlsx'

        # Save the workbook to the response
        wb.save(response)

        return response





