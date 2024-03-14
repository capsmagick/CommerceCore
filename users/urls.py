from django.urls import path, include
from django.conf import settings
from rest_framework.routers import DefaultRouter
from rest_framework.routers import SimpleRouter
from rest_framework_simplejwt.views import TokenRefreshView
from . import views

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register('user-address', views.AddressRegisterModelViewSet)
router.register('store-manager', views.StoreManagerViewSet)

urlpatterns = [
    path('user/sign-up/', views.Signup.as_view(), name='user-signup'),
    path('user/change-password/', views.ChangePassword.as_view(), name='change-password'),
    path('user/me/', views.Me.as_view(), name='me'),

    path(
        'session/', include(([
            path('user/login/', views.Login.as_view(), name='user-login')
        ])), name="session-login"
    ),

    path(
        'token/', include(([
            path('user/login/', views.TokenLoginAPTView.as_view(), name='token-login'),
            path('user/token/refresh/', TokenRefreshView.as_view(), name='token-refresh'),
        ])), name="jwt-token-login"
    ),

    path('social/', include('allauth.urls')),

    # path(
    #     'jwt/', include(([
    #         path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    #         path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    #     ])), name='jwt-login'
    # )
]

urlpatterns += router.urls

