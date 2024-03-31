from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('order', views.OrderModelViewSet)
router.register('placeorder', views.PlaceOrder)

urlpatterns = []
urlpatterns += router.urls