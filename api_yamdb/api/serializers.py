from rest_framework import serializers
from reviews.models import Category, Genre, Title
from users.models import User

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Category
        lookup_field = 'slug'


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        exclude = ('id', )
        model = Genre
        lookup_field = 'slug'


class TitleReadSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)
    genre = GenreSerializer(
        read_only=True,
        many=True
    )
    rating = serializers.IntegerField(read_only=True)

    class Meta:
        fields = '__all__'
        model = Title


class TitleWriteSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='slug'
    )
    genre = serializers.SlugRelatedField(
        queryset=Genre.objects.all(),
        slug_field='slug',
        many=True
    )

    class Meta:
        fields = '__all__'
        model = Title

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'role',
            'username',
            'email',
            'bio',
            'first_name',
            'last_name'
        )


class RegisterSerializer(serializers.ModelSerializer):
    username = serializers.CharField(
        queryset=User.objects.all()
    )
    email = serializers.EmailField(
        queryset=User.objects.all()
    )

    def validate_username(self, value):
        if value.lower() == 'me':
            raise serializers.ValidationError(
                'Никнейм не может быть "me"'
            )
        return value

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
