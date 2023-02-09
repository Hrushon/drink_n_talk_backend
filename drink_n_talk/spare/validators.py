from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy


def validate_birthday(value):
    """
    Валидатор для дней рождения. Возраст пользователя не может быть меньше
    18 лет.
    """
    eighteen_years_ago = date.today() - timedelta(days=5475)
    if value > eighteen_years_ago:
        raise ValidationError(
            gettext_lazy(
                'Возраст меньше 18 лет. Дата рождения: %(value)s'
            ), params={'value': value}
        )
