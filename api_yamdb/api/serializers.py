from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from reviews.models import Category, Genre, Title
from users.models import User


class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadOnlySerializer(serializers.ModelSerializer):
    category = CategorySerializer(
        read_only=True,
    )
    genre = GenreSerializer(
        many=True,
        read_only=True,
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug',
        required=True,
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True,
        required=False,
    )

    class Meta:
        fields = '__all__'
        model = Title


class UserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True)
    email = serializers.EmailField(
        validators=[
            UniqueValidator(queryset=User.objects.all())
        ],
        required=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )


class UserSerializerOrReadOnly(serializers.ModelSerializer):

    role = serializers.CharField(read_only=True)

    class Meta:
        model = User
        fields = (
            'first_name',
            'last_name',
            'username',
            'bio',
            'email',
            'role'
        )


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'username']

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Никнейм не может быть "me"'
            )
        return value

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

    class Meta:
        fields = ('username', 'email')
        model = User
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=User.objects.all(),
                fields=['username', 'email']
            )
        ]


class ConfirmationSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=30)
    confirmation_code = serializers.CharField()

    class Meta:
        model = User
        fields = ('username', 'confirmation_code')
