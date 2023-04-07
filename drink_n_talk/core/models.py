from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

User = get_user_model()


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

    class Meta:
        """
        Сортирует и добавляет названия в админке.
        """
        ordering = ('title',)
        verbose_name = 'тема'
        verbose_name_plural = 'темы'

    def __str__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.title} ({self.tag})>'


class Bar(models.Model):
    """Барная стойка, стол, за которым собираются пользователи."""

    title = models.CharField(
        max_length=256,
        verbose_name='название стойки'
    )
    initiator = models.OneToOneField(
        User,
        related_name='own_bar',
        on_delete=models.CASCADE,
        verbose_name='инициатор'
    )
    participants = models.ManyToManyField(
        User,
        through='BarParticipant',
        verbose_name='участники'
    )
    theme = models.ManyToManyField(
        Theme,
        through='BarTheme',
        verbose_name='темы разговора'
    )
    degree = models.PositiveSmallIntegerField(
        choices=settings.DEGREE_CHOICES,
        verbose_name='степень алкогольности'
    )
    about = models.CharField(
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
    picture = models.ImageField(
        upload_to='bars_pictures',
        default='bars_pictures/default_picture.jpg',
        verbose_name='картинка'
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
        return f'<{self.title} ({self.initiator})>'


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


class BarTheme(models.Model):
    """
    Промежуточная модель для связывания тем и барной стойки.
    """
    bar = models.ForeignKey(
        Bar,
        on_delete=models.CASCADE,
        verbose_name='бар'
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
        verbose_name = 'бар + тема'
        verbose_name_plural = 'бары + темы'

        constraints = [
            models.UniqueConstraint(
                fields=['bar', 'theme'],
                name='unique_bar_theme'
            )
        ]

    def __str__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.bar} + {self.theme}>'
