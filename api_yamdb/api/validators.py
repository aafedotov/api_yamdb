from datetime import date

from rest_framework.serializers import ValidationError

from reviews.models import Category


def category_slug_validator(value):
    """Проверяем уникальность слага."""
    if Category.objects.filter(slug=value).exists():
        raise ValidationError('Slug не уникален.')
    return value


def title_year_validator(value):
    """Проверяем валидность года выпуска."""
    year_now = date.today().year
    if value > year_now or value < 0:
        raise ValidationError(
            'Год выпуска не может быть больше текущего!')
    return value
