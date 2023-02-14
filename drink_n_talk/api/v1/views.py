from rest_framework import viewsets

from core.models import Drink, Language, Theme

from .serializers import DrinkSerializer, LanguageSerializer, ThemeSerializer


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для языков общения пользователей.

    Обрабатывает GET-запрос на получение списка языков.
    """
    serializer_class = LanguageSerializer
    queryset = Language.objects.all()


class DrinkViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для напитков.

    Обрабатывает GET-запрос на получение списка напитков.
    """
    serializer_class = DrinkSerializer
    queryset = Drink.objects.all()


class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для тем общения.

    Обрабатывает GET-запросы на получение списка доступных тем для разговоров.
    """
    serializer_class = ThemeSerializer
    queryset = Theme.objects.all()
