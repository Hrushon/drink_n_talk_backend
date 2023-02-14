from django.contrib.auth import get_user_model
from djoser.views import UserViewSet
from rest_framework import serializers

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """
    Кастомизированное представление библиотеки djoser для пользователей.
    """

    pass
