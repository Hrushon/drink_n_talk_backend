from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомизация базовой модели пользователя."""

    sex = models.SmallIntegerField(
        choices=settings.SEX_CHOICES,
        verbose_name='мужчина/женщина',
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
