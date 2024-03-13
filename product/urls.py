from django.conf import settings
from django.urls import path
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('product', views.ProductsModelViewSet)
router.register('variant', views.VariantModelViewSet)
router.register('product-image', views.ProductImageModelViewSet)
router.register('collection', views.CollectionModelViewSet)
router.register('look-book', views.LookBookModelViewSet)

urlpatterns = [
    path('import/product/', views.ImportProduct.as_view(), name='import-product'),
]
urlpatterns += router.urls
