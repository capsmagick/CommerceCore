from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('order', views.OrderModelViewSet)
router.register('orderitems', views.OrderItemModelSerializer)

urlpatterns = []
urlpatterns += router.urls