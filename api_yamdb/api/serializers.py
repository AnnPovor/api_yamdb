from rest_framework import serializers
from users.models import User


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
