from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.exceptions import NotFound
from django.core.paginator import InvalidPage


class CustomPagination(PageNumberPagination):
    default_limit = 10  # Set your default page size here
    max_limit = 100  # Set the maximum allowed page size here
    limit_query_param = 'limit'
    offset_query_param = 'offset'
    page_size_query_param = 'per_page'

    def get_limit(self, request):
        if self.limit_query_param:
            try:
                limit = int(request.query_params[self.limit_query_param])
                return min(limit, self.max_limit)
            except (KeyError, ValueError):
                pass

        return self.default_limit

    def get_offset(self, request):
        try:
            return int(request.query_params[self.offset_query_param])
        except (KeyError, ValueError):
            return 0

    def get_page_size(self, request):
        if self.page_size_query_param:
            try:
                size = int(request.query_params[self.page_size_query_param])
                return self.total_count if size == -1 else size
            except (KeyError, ValueError):
                pass

        return self.page_size

    def get_query(self, request, queryset):
        if self.limit_query_param in request.query_params:
            return queryset[self.offset:self.offset + self.limit]

        return queryset

    def paginate_queryset(self, queryset, request, view=None):
        self.total_count = self.get_total_count(queryset) # noqa

        self.limit = self.get_limit(request) # noqa
        if not self.limit:
            return None

        page_size = self.get_page_size(request)
        if not page_size:
            return None

        self.offset = self.get_offset(request) # noqa

        if self.total_count == 0 or self.offset > self.total_count:
            paginator = self.django_paginator_class([], page_size)
        else:
            paginator = self.django_paginator_class(
                self.get_query(request, queryset), page_size
            )

        page_number = self.get_page_number(request, paginator)

        try:
            self.page = paginator.page(page_number)
        except InvalidPage as exc:
            msg = self.invalid_page_message.format(
                page_number=page_number, message=str(exc)
            )
            raise NotFound(msg)

        if paginator.num_pages > 1 and self.template is not None:
            # The browsable API should display pagination controls.
            self.display_page_controls = True

        self.request = request
        return list(self.page)

    def get_total_pages(self):
        if self.limit is None:
            return None
        total_pages = divmod(self.page.paginator.count, self.limit)[0]
        if self.page.paginator.count % self.limit > 0:
            total_pages += 1
        return total_pages

    def get_total_count(self, queryset):
        try:
            return queryset.count()
        except Exception as e:
            return len(queryset)

    def get_paginated_response(self, data):
        return Response({
            'total_pages': self.get_total_pages(),
            'total': self.total_count,  # Here is your total count
            'results': data,
            'previous': self.get_previous_link(),
            'next': self.get_next_link(),
        })

