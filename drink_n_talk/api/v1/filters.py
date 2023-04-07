from django.conf import settings
from django_filters import rest_framework as filters

from core.models import Bar, Theme


class BarFilter(filters.FilterSet):
    """Кастомный фильтр для представления рецептов."""

    themes = filters.ModelMultipleChoiceFilter(
        field_name='theme__tag',
        queryset=Theme.objects.all(),
        to_field_name='tag'
    )
    degree = filters.MultipleChoiceFilter(
        choices=settings.DEGREE_CHOICES,
        conjoined=True
    )

    class Meta:
        model = Bar
        fields = ['degree']
