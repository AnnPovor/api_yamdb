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

    def get_serializer_class(self):
        if self.action in ('list', 'retrieve'):
            return TitleReadSerializer
        return TitleWriteSerializer


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAdmin,)
    filter_backends = (filters.SearchFilter,)
    lookup_field = 'username'
    lookup_value_regex = '[^/]+'
    search_fields = ["=username", ]

    @action(
        methods=['get', 'patch'],
        detail=False,
        permission_classes=[IsAuthenticated],
    )
    def me(self, request):
        serializer = UserSerializerOrReadOnly(request.user)
        if request.method == "PATCH":
            serializer = UserSerializerOrReadOnly(
                request.user,
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
def register(request):
    serializer = RegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    user = get_object_or_404(
        User,
        username=serializer.validated_data["username"]
    )
    confirmation_code = default_token_generator.make_token(user)
    send_mail(
        subject='Регистрация на сайте YaMDb',
        message=f'Код подтверждения: {confirmation_code}!',
        from_email=ADMIN_EMAIL,
        recipient_list=[user.email],
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
    confirmation_code = serializer.data['confirmation_code']
    if default_token_generator.check_token(user, confirmation_code):
        token = RefreshToken.for_user(user)
        return Response(
            {'token': str(token.access_token)}, status=status.HTTP_200_OK
        )
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)