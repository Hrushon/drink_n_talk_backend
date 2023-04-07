from rest_framework import serializers

from core.models import Bar, Drink, Theme
from users.serializers import UserSerializer


class DrinkSerializer(serializers.ModelSerializer):
    """Сериализатор для напитков."""

    class Meta:
        model = Drink
        fields = ('title', 'degree',)


class ThemeSerializer(serializers.ModelSerializer):
    """Сериализатор для тем общения."""

    class Meta:
        model = Theme
        fields = ('title', 'tag')


class BarSerializer(serializers.ModelSerializer):
    """Сериализатор для барных стоек."""

    initiator = UserSerializer()
    participants = UserSerializer(many=True)
    theme = ThemeSerializer(many=True)

    class Meta:
        model = Bar
        fields = '__all__'


class BarCreateSerializer(serializers.ModelSerializer):
    """Сериализатор для создания барных стоек."""

    initiator = UserSerializer(
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    participants = UserSerializer(
        default=serializers.CurrentUserDefault(),
        read_only=True
    )
    theme = serializers.SlugRelatedField(
        queryset=Theme.objects.all(),
        slug_field='tag',
        many=True
    )

    class Meta:
        model = Bar
        fields = '__all__'

    def to_representation(self, instance):
        """
        После создания объект барной стойки сериализуется через
        `BarSerializer`.
        """
        return BarSerializer(instance, context=self.context).data
