from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    CategoryViewSet,
    GenreViewSet,
    TitleViewSet
)

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

urlpatterns = [
    path('v1/', include(v1_router.urls)),
]
