from django.contrib.auth import get_user_model
from djoser.serializers import UserCreateSerializer
from rest_framework import serializers

User = get_user_model()


class CustomUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор для создания пользователя."""

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
            'password',
            'about',
            'photo',
            'birth_day',
            'degree',
            'character'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'first_name',
            'last_name',
            'email',
            'about',
            'photo',
            'birth_day',
            'degree',
            'character'
        )
