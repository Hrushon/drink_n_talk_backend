from django.contrib.auth import get_user_model
from djoser.views import UserViewSet

User = get_user_model()


class CustomUserViewSet(UserViewSet):
    """
    Кастомизированное представление библиотеки djoser для пользователей.
    """

    pass
