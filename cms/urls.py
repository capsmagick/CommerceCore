from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('hero-section', views.HeroSectionModelViewSet)
router.register('customer/hero-section', views.HeroSectionCustomer)

urlpatterns = []
urlpatterns += router.urls