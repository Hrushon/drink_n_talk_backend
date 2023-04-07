from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'email',
            'sex',
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'sex',
            'password',
        )

    def to_representation(self, instance):
        """
        После создания объект пользователя сериализуется через
        `UserSerializer`.
        """
        return UserSerializer(instance, context=self.context).data
