from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend 
from rest_framework import (filters, permissions, status)
from rest_framework import mixins, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet
from rest_framework.pagination import PageNumberPagination, LimitOffsetPagination

from api_yamdb.settings import ADMIN_EMAIL
from reviews.models import Category, Genre, Title
from users.models import User
from .permissions import IsAdmin
from .permissions import IsAdminUserOrReadOnly
from .serializers import (
    CategorySerializer,
    GenreSerializer,
    TitleReadSerializer,
    TitleWriteSerializer,
    RegisterSerializer,
    ConfirmationSerializer,
    UserSerializer,
    UserSerializerOrReadOnly
)


class CustomViewSet(
    CreateModelMixin,
    ListModelMixin,
    DestroyModelMixin,
    GenericViewSet
):
    pass


class CreateViewSet(
    mixins.CreateModelMixin,
    viewsets.GenericViewSet
):
    pass


class CategoryViewSet(CustomViewSet):
# class CategoryViewSet(viewsets.ModelViewSet):

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


class TitleViewSet(CustomViewSet):

    queryset = Title.objects.all()
    pagination_class = LimitOffsetPagination
    permission_classes = (IsAdminUserOrReadOnly,)
    filter_backends = (DjangoFilterBackend,)
    search_fields = ('name', )
    lookup_field = 'slug'

    def get_serializer_class(self):
        if self.request.method in (
            'POST',
            'PATCH',
            'DELETE'
        ):
            return TitleWriteSerializer
        return TitleReadSerializer


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
    if (user.confirmation_code != serializer.validated_data['confirmation_code']
        ):
        return Response(status=status.HTTP_400_BAD_REQUEST)

    return Response(
        {'token': str(user.token)}, status=status.HTTP_200_OK
    )


class UserViewSet(viewsets.ModelViewSet):
    # permission_classes = (IsAdmin,)
    # # queryset = User.objects.all()
    # serializer_class = UserSerializer
    # lookup_field = 'username'
    # # pagination_class = PageNumberPagination
    # pagination_class = LimitOffsetPagination
    # filter_backends = (filters.SearchFilter,)
    # search_fields = ('username',)

    # @action(
    #     methods=['get', 'patch'],
    #     detail=False,
    #     permission_classes=[IsAuthenticated],
    #     serializer_class=UserSerializerOrReadOnly
    # )
    # def get_queryset(self):
    #     queryset = User.objects.all()
    #     return queryset

    # def users_profile(self, request):
    #     user = request.user
    #     if request.method == "GET":
    #         serializer = self.get_serializer(user)
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     if request.method == "PATCH":
    #         serializer = self.get_serializer(
    #             user,
    #             data=request.data,
    #             partial=True
    #         )
    #         serializer.is_valid(raise_exception=True)
    #         serializer.save()
    #         return Response(serializer.data, status=status.HTTP_200_OK)
    #     return Response(status=status.HTTP_405_METHOD_NOT_ALLOWED)
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated, IsAdmin,)
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    filter_backends = (filters.SearchFilter, )
    search_fields = ('username', )

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
