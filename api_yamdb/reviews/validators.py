from datetime import date

from django.core.exceptions import ValidationError


def validate_year(value):
    """Валидируем год."""
    year_now = date.today().year
    if year_now < value:
        raise ValidationError('Год выпуска не может быть больше текущего!')
    return value
