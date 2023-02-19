from rest_framework import serializers

from core.models import Bar, Drink, Language, Theme


class LanguageSerializer(serializers.ModelSerializer):
    """Сериализатор для языков общения."""

    class Meta:
        model = Language
        fields = ('name', 'abbreviation')


class DrinkSerializer(serializers.ModelSerializer):
    """Сериализатор для напитков."""

    class Meta:
        model = Drink
        fields = ('title', 'degree')


class ThemeSerializer(serializers.ModelSerializer):
    """Сериализатор для тем общения."""

    class Meta:
        model = Theme
        fields = ('title', 'tag')


class BarSerializer(serializers.ModelSerializer):
    """Сериализатор для барных стоек."""

    class Meta:
        model = Bar
        fields = '__all__'
