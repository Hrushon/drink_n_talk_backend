from django.conf import settings
from django.db.models import Count, F
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Bar, BarParticipant, Drink, Theme
from .filters import BarFilter
from .permissions import IsInitiatorOrAdminOnlyPermission
from .serializers import (BarCreateSerializer, BarSerializer, DrinkSerializer,
                          ThemeSerializer)


class DrinkViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для напитков.

    Обрабатывает GET-запрос на получение списка напитков.
    """

    serializer_class = DrinkSerializer
    queryset = Drink.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ['^title', 'title']


class ThemeViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для тем общения.

    Обрабатывает GET-запросы на получение списка доступных тем для разговоров.
    """

    serializer_class = ThemeSerializer
    queryset = Theme.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ['^title', 'title']


class BarViewSet(viewsets.ModelViewSet):
    """
    Представление для барных стоек.

    Обрабатывает GET, POST, DELETE - запросы для работы с барными стойками.
    """

    serializer_class = BarSerializer
    permission_classes = (IsAuthenticated,)
    filter_backends = (DjangoFilterBackend,)
    filterset_class = BarFilter
    http_method_names = ['get', 'post', 'delete']

    def get_permissions(self):
        if self.action != 'to_join' and self.request.method == 'DELETE':
            self.permission_classes = (IsInitiatorOrAdminOnlyPermission,)
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'barparticipant'):
            return user.bar_set.all()
        return Bar.objects.annotate(
            current_quantity=Count('participants')
        ).filter(
            quantity__gt=F('current_quantity')
        ).order_by('-current_quantity')

    def get_serializer_class(self):
        if self.action == 'create':
            return BarCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        if hasattr(request.user, 'own_bar'):
            raise serializers.ValidationError(
                {
                    'errors': [
                        'У Вас уже есть активная барная стойка.'
                    ]
                }
            )
        return super().create(request, *args, **kwargs)

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
        """
        Дополнительный маршрут для присоединения/отсоединения участника
        к барной стойке.
        """
        participant = request.user
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
