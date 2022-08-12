from django.core.mail import send_mail
# from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, permissions, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.mixins import (CreateModelMixin, DestroyModelMixin,
                                   ListModelMixin)
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from reviews.models import Category, Genre, Title
from users.models import User

from api_yamdb.settings import ADMIN_EMAIL

from .filters import TitleFilter
from .permissions import IsAdmin, IsAdminUserOrReadOnly
from .serializers import (CategorySerializer, ConfirmationSerializer,
                          GenreSerializer, RegisterSerializer,
                          TitleReadOnlySerializer, TitleWriteSerializer,
                          UserSerializer, UserSerializerOrReadOnly)


class CustomViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    pass


class CategoryViewSet(CustomViewSet):

    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class GenreViewSet(CustomViewSet):

    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', )
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):

    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    serializer_class = TitleReadOnlySerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter

    @action(
        methods=[
            'POST',
            'PATCH',
            'DELETE'],
        detail=True,
        permission_classes=[IsAdmin],
    )
    def post_admin(self, request):
        if request.user.is_admin:
            serializer = TitleWriteSerializer(
                request.user,
                data=request.data,
                partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def register(request):
    serializer = RegisterSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = User.objects.get(email=serializer.validated_data['email'])
    send_mail(
        subject='Регистрация на сайте YaMDb',
        message=f'Код подтверждения: {user.confirmation_code}!',
        from_email=ADMIN_EMAIL,
        recipient_list=[user.email]
    )
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([permissions.AllowAny])
def get_token(request):
    serializer = ConfirmationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    if (
        user.confirmation_code != serializer.validated_data
        ['confirmation_code']
    ):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {'token': str(user.token)}, status=status.HTTP_200_OK
    )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

    @action(
        methods=['get', 'patch'],
        detail=True,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer = UserSerializerOrReadOnly(request.user)
        if request.method == "PATCH":
            serializer = UserSerializerOrReadOnly(
                request.user,
            )
        return Response(serializer.data)

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=(IsAuthenticated,),
        url_path='me')
    def get_current_user_info(self, request):
        serializer = UserSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserSerializer(
                    request.user,
                    data=request.data,
                    partial=True)
            else:
                serializer = UserSerializerOrReadOnly(
                    request.user,
                    data=request.data,
                    partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data)
