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
            'name',
            'surname',
            'email',
            'password',
            'about',
            'photo',
            'birth_day',
            'degree',
            'silent_talker'
        )


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    class Meta:
        model = User
        fields = (
            'id',
            'username',
            'name',
            'surname',
            'email',
            'about',
            'photo',
            'birth_day',
            'degree',
            'silent_talker'
        )
