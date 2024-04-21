from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('category', views.CategoryModelViewSet)
router.register('brand', views.BrandModelViewSet)
# router.register('tag', views.TagModelViewSet)
router.register('attribute', views.AttributeModelViewSet)
router.register('attributegroup', views.AttributeGroupModelViewSet)
router.register('dimension', views.DimensionModelViewSet)
router.register('return-reasons', views.ReturnReasonModelViewSet)

urlpatterns = []
urlpatterns += router.urls