from django.urls import path

from drf_spectacular.views import SpectacularAPIView
from drf_spectacular.views import SpectacularRedocView
from drf_spectacular.views import SpectacularSwaggerView

from . import rest_api as views


urlpatterns = [
    path('docs/api/schema/', SpectacularAPIView.as_view(), name='schema'),
    path('docs/api/schema/swagger-ui/', SpectacularSwaggerView.as_view(url_name='schema'), name='swagger-ui'),
    path('docs/api/schema/redoc/', SpectacularRedocView.as_view(url_name='schema'), name='redoc'),
]

urlpatterns += [
    path('import/table-data/', views.ImportTableData.as_view(), name='import-table-data'),
]
