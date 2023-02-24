from django.conf import settings
from django.db.models import Count, F, Sum
from rest_framework import serializers, status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import SearchFilter
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from core.models import Bar, BarParticipant, Drink, Language, Theme, UserDrink
from .permissions import IsInitiatorOrAdminOnlyPermission
from .serializers import (BarCreateSerializer, BarSerializer, DrinkSerializer,
                          LanguageSerializer, ThemeSerializer)


class LanguageViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для языков общения пользователей.

    Обрабатывает GET-запрос на получение списка языков.
    """

    serializer_class = LanguageSerializer
    queryset = Language.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ['^name', 'name']


class DrinkViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Представление для напитков.

    Обрабатывает GET-запрос на получение списка напитков.
    """

    serializer_class = DrinkSerializer
    queryset = Drink.objects.all()
    filter_backends = (SearchFilter,)
    search_fields = ['^title', 'title']

    def get_permissions(self):
        if self.action == 'pour':
            self.permission_classes = (IsAuthenticated,)
        return super().get_permissions()

    @action(
        methods=['get', 'delete'],
        detail=True
    )
    def pour(self, request, pk):
        """
        Дополнительный маршрут для связывания пользователя с
        выбранным напитком.
        """
        user = request.user
        drink = self.get_object()
        instance = False
        if hasattr(user, 'userdrink'):
            instance = user.userdrink
        if request.method == 'DELETE':
            if not instance or instance.drink != drink:
                raise serializers.ValidationError(
                    {
                        'errors': [
                            'Вы не употребляете этот напиток.'
                        ]
                    }
                )
            instance.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        if instance:
            if instance.drink == drink:
                raise serializers.ValidationError(
                    {
                        'errors': [
                            'Вы уже употребляете этот напиток.'
                        ]
                    }
                )
            instance.delete()
        UserDrink.objects.create(
            user=user,
            drink=drink
        )
        serializer = self.get_serializer(drink)
        return Response(serializer.data, status=status.HTTP_200_OK)


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

    serializer_class = BarSerializer
    permission_classes = (IsAuthenticated,)
    http_method_names = ['get', 'post', 'delete']

    def get_permissions(self):
        if self.request.method == 'DELETE':
            return IsInitiatorOrAdminOnlyPermission
        return super().get_permissions()

    def get_queryset(self):
        user = self.request.user
        if hasattr(user, 'barparticipant'):
            return list(user.barparticipant.bar)
        languages = user.language_set.all()
        degree = user.degree
        if hasattr(user, 'userdrink'):
            degree = user.userdrink
        themes = user.theme_set.all()
        order_type = '-current_characters'
        if user.character == settings.TALKER:
            order_type = 'current_characters'
        return Bar.objects.annotate(
            current_quantity=Count('participants')
        ).annotate(
            current_characters=Sum('participants__character')
        ).filter(
            **{'language__in': languages},
            **{'degree__gte': degree},
            **{'theme__in': themes},
        ).filter(
            quantity__gt=F('current_quantity')
        ).order_by(order_type)

    def get_serializer_class(self):
        if self.action == 'create':
            return BarCreateSerializer
        return super().get_serializer_class()

    def create(self, request, *args, **kwargs):
        if not request.data.get('degree'):
            degree = request.user.degree
            if hasattr(request.user, 'userdrink'):
                degree = request.user.userdrink.drink.degree
            request.data['degree'] = degree
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
