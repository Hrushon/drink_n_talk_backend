from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    """Кастомизация базовой модели пользователя."""

    birth_day = models.DateField()
    about = models.TextField(
        blank=True
    )
    photo = models.ImageField(
        upload_to='users_photos',
        default='default_user.jpg'
    )

    def __repr__(self):
        """
        Добавляет удобочитаемый вывод при вызове экземпляра объекта
        на печать и в оболочке shell.
        """
        return f'< userid = {self.id}  | username = {self.username} >'

    class Meta:
        """
        Сортирует и добавляет названия в админке.
        """
        ordering = ('-id',)
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
