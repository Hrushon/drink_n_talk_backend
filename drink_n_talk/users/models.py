from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models

from spare.validators import validate_birthday


class User(AbstractUser):
    """Кастомизация базовой модели пользователя."""

    birth_day = models.DateField(
        verbose_name='день рождения',
        validators=[validate_birthday]
    )
    about = models.TextField(
        blank=True,
        max_length=254,
        verbose_name='о себе'
    )
    photo = models.ImageField(
        upload_to='users_photos',
        default='user_avatar/default_user.jpg',
        verbose_name='аватар'
    )
    degree = models.PositiveSmallIntegerField(
        choices=settings.DEGREE_CHOICES,
        default=settings.DEFAULT_DEGREE,
        verbose_name='степень алкогольности'
    )
    character = models.SmallIntegerField(
        choices=settings.CHARACTER_CHOICES,
        verbose_name='слушатель/говорун'
    )

    class Meta:
        """
        Сортирует и добавляет названия в админке.
        """
        ordering = ('-id',)
        verbose_name = 'пользователь'
        verbose_name_plural = 'пользователи'

    def __str__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'<user.id = {self.id} | username = {self.username}>'
