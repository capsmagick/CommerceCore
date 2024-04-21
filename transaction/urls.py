from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('details', views.TransactionModelViewSet)

# ShipRocket
router.register('shiprocket', views.ShipRocketViewSet, basename='shiprocket')


urlpatterns = [
    path('payment/initiate/', views.TransactionAPIView.as_view(), name='transaction-initiate'),
    path('payment/callback/', views.TransactionCallBackAPIView.as_view(), name='transaction-callback'),
]
urlpatterns += router.urls


