
from rest_framework.routers import DefaultRouter

from django.urls import include, path

from .views import (UserViewSet, register, get_token, CategoryViewSet,GenreViewSet, TitleViewSet)

app_name = 'api'

v1_router = DefaultRouter()


v1_router.register(
    'categories',
    CategoryViewSet,
    basename='сategories'
)
v1_router.register(
    'titles',
    TitleViewSet,
    basename='titles'
)
v1_router.register(
    'genres',
    GenreViewSet,
    basename='genres'
)


v1_router.register('users', UserViewSet, basename='users')


urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/', include('djoser.urls.jwt')),
    path('v1/auth/signup/', register, name='register'),
    path('v1/auth/token/', get_token, name='token')
    ]
