from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Bar, BarParticipant, Drink, Language, Theme
from .serializers import (BarCreateSerializer, BarSerializer, DrinkSerializer,
                          LanguageSerializer, ThemeSerializer)


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


class BarViewSet(viewsets.ModelViewSet):
    """
    Представление для барных стоек.

    Обрабатывает GET, POST, DELETE - запросы для работы с барными стойками.
    """

    queryset = Bar.objects.all()
    serializer_class = BarSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'delete']

    def get_serializer_class(self):
        if self.action == 'create':
            return BarCreateSerializer
        return super().get_serializer_class()

    def perform_create(self, serializer):
        instance = serializer.save(initiator=self.request.user)
        BarParticipant.objects.create(
            bar=instance,
            participant=self.request.user
        )

    @action(
        methods=['get', 'delete'],
        detail=True
    )
    def to_join(self, request, pk):
        participant = self.request.user
        bar = self.get_object()
        instance = False
        if hasattr(participant, 'barparticipant'):
            instance = participant.barparticipant
        if request.method == 'DELETE':
            if not instance or instance.bar != bar:
                raise serializers.ValidationError(
                    {
                        'errors': [
                            'Вы не являетесь участником данной беседы.'
                        ]
                    }
                )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if instance:
            raise serializers.ValidationError(
                {
                    'errors': [
                        'Вы уже являетесь участником беседы.'
                    ]
                }
            )
        BarParticipant.objects.create(
            bar=bar,
            participant=participant
        )
        serializer = self.get_serializer(bar)
        return Response(serializer.data, status=status.HTTP_200_OK)
