from django.contrib.auth import get_user_model
from django.contrib.auth.validators import UnicodeUsernameValidator
from djoser.serializers import TokenCreateSerializer, UserCreateSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from core.models import Language, Theme, UserLanguage, UserTheme

User = get_user_model()


class UserLanguageSerializer(serializers.ModelSerializer):
    """Сериализатор для языков при отображении данных пользователя."""

    class Meta:
        model = Language
        fields = ('name', 'abbreviation')


class UserThemeSerializer(serializers.ModelSerializer):
    """Сериализатор для тем при отображении данных пользователя."""

    class Meta:
        model = Theme
        fields = ('title', 'tag')


class UserSerializer(serializers.ModelSerializer):
    """Сериализатор для пользователей."""

    login = serializers.CharField(source='username')
    theme = UserThemeSerializer(
        many=True,
        read_only=True,
        source='theme_set'
    )
    language = UserLanguageSerializer(
        many=True,
        read_only=True,
        source='language_set'
    )

    class Meta:
        model = User
        fields = (
            'id',
            'login',
            'first_name',
            'last_name',
            'email',
            'about',
            'photo',
            'birth_day',
            'degree',
            'character',
            'theme',
            'language'
        )


class CustomUserCreateSerializer(UserCreateSerializer):
    """Кастомный сериализатор для создания пользователя."""

    login = serializers.CharField(
        help_text=('Обязательное поле. Не более 150 символов. '
                   'Только буквы, цифры и символы @/./+/-/_.'),
        label='Логин пользователя',
        max_length=150,
        validators=[
            UnicodeUsernameValidator,
            UniqueValidator(queryset=User.objects.all()),
        ],
        source='username',
    )
    theme = serializers.SlugRelatedField(
        queryset=Theme.objects.all(),
        many=True,
        slug_field='tag',
    )
    language = serializers.SlugRelatedField(
        queryset=Language.objects.all(),
        many=True,
        slug_field='abbreviation'
    )

    class Meta:
        model = User
        fields = (
            'login',
            'first_name',
            'last_name',
            'email',
            'password',
            'about',
            'photo',
            'birth_day',
            'degree',
            'character',
            'theme',
            'language'
        )

    def to_representation(self, instance):
        """
        После создания объект пользователя сериализуется через
        `UserSerializer`.
        """
        return UserSerializer(instance, context=self.context).data

    def perform_create(self, validated_data):
        languages = validated_data.pop('language')
        themes = validated_data.pop('theme')
        user = super().perform_create(validated_data)
        for language in languages:
            UserLanguage.objects.create(
                user=user,
                language=language
            )
        for theme in themes:
            UserTheme.objects.create(
                user=user,
                theme=theme
            )
        return user

    def update(self, instance, validated_data):
        languages = validated_data.pop('language', None)
        themes = validated_data.pop('theme', None)
        if languages:
            instance.language_set.set(languages)
        if themes:
            instance.theme_set.set(themes)
        return super().update(instance, validated_data)


class TokenUserCreateSerializer(TokenCreateSerializer):
    """Кастомизация сериализатора для создания токена пользователю."""

    def __init__(self, *args, **kwargs):
        super(serializers.Serializer, self).__init__(*args, **kwargs)
        self.user = None
        self.fields['login'] = serializers.CharField(required=False)

    def validate(self, attrs):
        """Позволяет изменить `username` на `login`."""
        username = attrs.get('login')
        attrs['username'] = username
        return super().validate(attrs)
