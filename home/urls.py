from django.urls import path
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

urlpatterns = [
    path('dashboard/', views.DashboardAPIView.as_view(), name='dashboard'),
    path('customer-growth/', views.CustomerGrowthAPIView.as_view(), name='customer-growth'),
    path('customer-order-analysis/', views.CustomerOrderAnalysisAPIView.as_view(), name='customer-order-analysis'),
]

urlpatterns += router.urls


