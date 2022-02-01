from django.core.exceptions import ValidationError


def validate_username(value):
    """Проверяем, что username != 'me'."""
    if value == 'me':
        raise ValidationError('username "me" недоступен для регистрации!')
    return value
