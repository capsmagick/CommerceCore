from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('tax', views.TaxModelViewSet)
router.register('warehouse', views.WarehouseModelViewSet)
router.register('batch', views.BatchModelViewSet)
router.register('inventory', views.InventoryModelViewSet)

urlpatterns = []
urlpatterns += router.urls
