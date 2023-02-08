from django.conf import settings
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Language(models.Model):
    """Языковая модель."""

    name = models.CharField(
        unique=True,
        max_length=20,
        verbose_name='Название'
    )
    abbreviation = models.SlugField(
        max_length=5,
        verbose_name='Аббревиатура'
    )
    users = models.ManyToManyField(
        User,
        through='UserLanguage',
        verbose_name='Пользователь(и)'
    )

    class Meta:
        """
        Сортирует и добавляет названия в админке.
        """
        ordering = ('abbreviation',)
        verbose_name = 'Язык'
        verbose_name_plural = 'Языки'

    def __repr__(self):
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
        verbose_name='Пользователь'
    )
    language = models.ForeignKey(
        Language,
        on_delete=models.CASCADE,
        verbose_name='Язык'
    )

    class Meta:
        """
        Добавляет названия в админке.
        """
        verbose_name = 'Пользователь + язык'
        verbose_name_plural = 'Пользователи + языки'
    
    def __repr__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.user} ({self.language})>'


class Drink(models.Model):
    """Модель для напитков."""

    title = models.CharField(
        max_length=20,
        verbose_name='Название'
    )
    degree = models.IntegerField(
        choices=settings.DEGREE_CHOICES,
        verbose_name='Степень алкогольности'
    )

    class Meta:
        """
        Сортирует и добавляет названия в админке.
        """
        ordering = ('title',)
        verbose_name = 'Напиток'
        verbose_name_plural = 'Напитки'

    def __repr__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.title} ({self.degree})>'


class UserDrink(models.Model):
    """
    Промежуточная модель для присваивания пользователю
    предпочитаемых напитков.
    """

    user = models.ForeignKey(
        User,
        related_name='drinks',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    drink = models.ForeignKey(
        Drink,
        on_delete=models.CASCADE,
        verbose_name='Напиток'
    )

    class Meta:
        """
        Добавляет названия в админке.
        """
        verbose_name = 'Пользователь + напиток'
        verbose_name_plural = 'Пользователи + напитки'
    
    def __repr__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<{self.user} + {self.drink}>'
