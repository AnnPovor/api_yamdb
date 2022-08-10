from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import UserViewSet, register, get_token

app_name = 'api'

router = DefaultRouter()

router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_token, name='token')
    ]
