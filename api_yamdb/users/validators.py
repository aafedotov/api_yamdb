from django.core.exceptions import ValidationError


def validate_username(value):
    """Запрещает использовать имя "me" в качестве username."""
    if value == 'me':
        raise ValidationError(
            'Использовать имя "me" в качестве username запрещено!'
        )
    return value
