from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


class Language(models.Model):
    """Языковая модель."""

    name = models.CharField(
        unique=True,
        max_length=20,
        verbose_name='название'
    )
    abbreviation = models.SlugField(
        max_length=7,
        verbose_name='аббревиатура'
    )
    users = models.ManyToManyField(
        User,
        through='UserLanguage',
        verbose_name='пользователь(и)'
    )

    class Meta:
        """
        Сортирует и добавляет названия в админке.
        """
        ordering = ('abbreviation',)
        verbose_name = 'язык'
        verbose_name_plural = 'языки'

    def __str__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.name} ({self.abbreviation})>'


class UserLanguage(models.Model):
    """
    Промежуточная модель для присваивания пользователю разговорного языка.
    """

    user = models.ForeignKey(
        User,
        related_name='languages',
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        verbose_name='язык'
    )

    class Meta:
        """
        Добавляет названия в админке.
        """
        verbose_name = 'пользователь + язык'
        verbose_name_plural = 'пользователи + языки'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'language'],
                name='unique_user_language'
            )
        ]

    def __str__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.user} ({self.language})>'


class Drink(models.Model):
    """Модель для напитков."""

    title = models.CharField(
        max_length=20,
        verbose_name='название'
    )
    degree = models.PositiveSmallIntegerField(
        choices=settings.DEGREE_CHOICES,
        verbose_name='степень алкогольности'
    )
    users = models.ManyToManyField(
        User,
        through='UserDrink',
        verbose_name='пользователь(и)'
    )

    class Meta:
        """
        Сортирует и добавляет названия в админке.
        """
        ordering = ('title',)
        verbose_name = 'напиток'
        verbose_name_plural = 'напитки'

    def __str__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.title} ({self.degree})>'


class UserDrink(models.Model):
    """
    Промежуточная модель для присваивания пользователю
    потребялемого напитка.
    """

    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    drink = models.ForeignKey(
        Drink,
        on_delete=models.CASCADE,
        verbose_name='напиток'
    )

    class Meta:
        """
        Добавляет названия в админке.
        """
        verbose_name = 'пользователь + напиток'
        verbose_name_plural = 'пользователи + напитки'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'drink'],
                name='unique_user_drink'
            )
        ]

    def __str__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.user} + {self.drink}>'


class Theme(models.Model):
    """Модель для тем разговоров за Столом."""

    title = models.CharField(
        max_length=50,
        verbose_name='название темы'
    )
    tag = models.SlugField(
        max_length=50,
        verbose_name='сокращение (тег) для темы'
    )
    users = models.ManyToManyField(
        User,
        through='UserTheme',
        verbose_name='пользователь(и)'
    )

    class Meta:
        """
        Сортирует и добавляет названия в админке.
        """
        ordering = ('title',)
        verbose_name = 'напиток'
        verbose_name_plural = 'напитки'

    def __str__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.title} ({self.tag})>'


class UserTheme(models.Model):
    """
    Промежуточная модель для связывания пользователя и темы
    для разговора.
    """

    user = models.ForeignKey(
        User,
        related_name='themes',
        on_delete=models.CASCADE,
        verbose_name='пользователь'
    )
    theme = models.ForeignKey(
        Theme,
        on_delete=models.CASCADE,
        verbose_name='тема'
    )

    class Meta:
        """
        Добавляет названия в админке.
        """
        verbose_name = 'пользователь + тема'
        verbose_name_plural = 'пользователи + темы'

        constraints = [
            models.UniqueConstraint(
                fields=['user', 'theme'],
                name='unique_user_theme'
            )
        ]

    def __str__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.user} + {self.theme}>'


class Bar(models.Model):
    """Барная стойка, стол, за которым собираются пользователи."""

    initiator = models.OneToOneField(
        User,
        related_name='bars',
        on_delete=models.CASCADE,
        verbose_name='инициатор'
    )
    participants = models.ManyToManyField(
        User,
        through='BarParticipant',
        verbose_name='участники'
    )
    theme = models.ForeignKey(
        Theme,
        related_name='bars',
        on_delete=models.CASCADE,
        verbose_name='тема разговора'
    )
    degree = models.PositiveSmallIntegerField(
        choices=settings.DEGREE_CHOICES,
        verbose_name='степень алкогольности'
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        verbose_name='язык'
    )
    topic = models.CharField(
        max_length=254,
        verbose_name='повестка',
        blank=True
    )
    quantity = models.PositiveSmallIntegerField(
        verbose_name='количество участников за столом',
        default=settings.DEFAULT_COUNT_PARTICIPANTS,
        validators=[
            MinValueValidator(settings.MIN_COUNT_PARTICIPANTS),
            MaxValueValidator(settings.MAX_COUNT_PARTICIPANTS)
        ]
    )
    date_creation = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата создания'
    )

    class Meta:
        """
        Сортирует и добавляет названия в админке.
        """
        ordering = ('-id',)
        verbose_name = 'барная стойка'
        verbose_name_plural = 'барные стойки'

    def __str__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.theme} ({self.initiator})>'


class BarParticipant(models.Model):
    """
    Промежуточная модель для связывания участников и барной стойки.
    """
    bar = models.ForeignKey(
        Bar,
        on_delete=models.CASCADE,
        verbose_name='бар'
    )
    participant = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='участник'
    )
    date_join = models.DateTimeField(
        auto_now_add=True,
        verbose_name='дата присоединения'
    )

    class Meta:
        """
        Добавляет названия в админке.
        """
        verbose_name = 'бар + участник'
        verbose_name_plural = 'бары + участники'

        constraints = [
            models.UniqueConstraint(
                fields=['bar', 'participant'],
                name='unique_bar_participant'
            )
        ]

    def __str__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.bar} + {self.participant}>'
