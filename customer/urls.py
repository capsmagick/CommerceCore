from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter

from django.urls import path

from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('product', views.CustomerProductViewSet)
router.register('product-variants', views.CustomerVariantViewSet)
router.register('category', views.CustomerCategoryViewSet)
router.register('collections', views.CustomerCollectionViewSet)
router.register('lookbook', views.CustomerLookBookViewSet)
router.register('orders', views.CustomerOrderViewSet, basename='customer-orders')

router.register('cart', views.CartModelViewSet)
router.register('session/cart', views.SessionCartModelViewSet)
router.register('wishlist', views.WishListModelViewSet)

router.register('return-request', views.CustomerReturnViewSet)
router.register('manage/return-request', views.ManageCustomerReturn)

router.register('manage/reviews', views.ReviewModelViewSet)

urlpatterns = [
    path('add-review/', views.ReviewModelView.as_view(), name='add-review'),
]
urlpatterns += router.urls
