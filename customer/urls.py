from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('cart', views.CartModelViewSet)
router.register('wishlist', views.WishListModelViewSet)


urlpatterns = []
urlpatterns += router.urls
