from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомизация базовой модели пользователя."""

    birth_day = models.DateField(
        verbose_name='День рождения'
    )
    about = models.TextField(
        blank=True,
        verbose_name='О себе'
    )
    photo = models.ImageField(
        upload_to='/users_photos',
        default='default_user.jpg'б
        verbose_name='Аватар'
    )
    languages = models.ManyToManyField(
        'Language',
        through='UserLanguage',
        verbose_name='Язык(и)'
    )
    drinks = models.ManyToManyField(
        'Drink',
        through='UserDrink',
        verbose_name='Напиток(и)'
    )
    degree = models.IntegerField(
        choices=settings.DEGREE_CHOICES,
        verbose_name='Степень алкогольности'
    )

    class Meta:
        """
        Сортирует и добавляет названия в админке.
        """
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __repr__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<user.id = {self.id}  | username = {self.username}>'
