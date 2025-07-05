from django.urls import path, include
from rest_framework.routers import DefaultRouter

from .views import SignupViewSet, LoginViewSet, RefreshTokenViewSet


router = DefaultRouter()

router.register(r'register', SignupViewSet, basename='signup')
router.register(r'login', LoginViewSet, basename='login')
router.register(r'refresh', RefreshTokenViewSet, basename='refresh')


urlpatterns = [
    path('', include(router.urls))
]