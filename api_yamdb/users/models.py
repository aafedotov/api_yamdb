
from datetime import datetime
from datetime import timedelta

from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.conf import settings

import jwt

from .validators import validate_username


class CustomUserManager(BaseUserManager):
    """Описываем кастомную модель пользователя."""

    def create_user(self, email, username, role, bio, password=None):
        if not email:
            raise ValueError('e-mail обязателен для регистрации!')
        if not username:
            raise ValueError('username обязателен для регистрации!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            role=role,
            bio=bio,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class CustomUser(AbstractBaseUser):
    """Описываем кастомную модель пользователя."""
    email = models.EmailField(unique=True, max_length=60)
    username = models.CharField(unique=True, validators=[validate_username],
                                max_length=30)
    date_joined = models.DateTimeField(verbose_name='date joined',
                                       auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='last login', auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    ROLE_CHOICES = (
        ('user', 'Аутентифицированный пользователь'),
        ('moderator', 'Модератор'),
        ('admin', 'Администратор')
    )
    role = models.CharField(choices=ROLE_CHOICES,
                            default='user', max_length=64)
    bio = models.TextField(blank=True)
    first_name = models.CharField(max_length=150, blank=True)
    last_name = models.CharField(max_length=150, blank=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    @property
    def token(self):
        """Получаем токен пользователя через свойство."""
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """Создаем JWT-token для пользователя."""
        dt = datetime.now() + timedelta(days=60)
        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')
        return token.decode('utf-8')

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True






# from django.db import models
# from django.contrib.auth.models import AbstractUser
#
# from .validators import validate_username
#
#
# class CustomUser(AbstractUser):
#     """Описываем кастомную модель пользователя."""
#     ROLE_CHOICES = (
#         ('user', 'Аутентифицированный пользователь'),
#         ('moderator', 'Модератор'),
#         ('admin', 'Администратор')
#     )
#     email = models.EmailField(
#         max_length=254,
#         unique=True,
#         verbose_name='Email'
#     )
#     username = models.CharField(
#         max_length=150,
#         unique=True,
#         validators=[validate_username]
#     )
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     date_joined = models.DateTimeField(
#         auto_now_add=True,
#         verbose_name='date joined'
#     )
#     last_login = models.DateTimeField(
#         auto_now=True,
#         verbose_name='last login'
#     )
#     is_admin = models.BooleanField(default=False)
#     is_active = models.BooleanField(default=True)
#     is_staff = models.BooleanField(default=False)
#     is_superuser = models.BooleanField(default=False)
#
#     role = models.CharField(
#         max_length=10,
#         choices=ROLE_CHOICES,
#         default='user'
#     )
#     bio = models.TextField(
#         max_length=300,
#         null=True,
#         blank=True,
#         help_text='About myself'
#     )
#
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = ['email']
#
#     objects = CustomUserManager()
#
#     def __str__(self):
#         return self.username
#
#     def has_perm(self, perm, obj=None):  # Возвращает True если пользователь имеет указанное право доступа,
#         # где право указывает в формате "<app label>.<permission codename>".
#         # (смотрите раздел Права пользователя ниже). Если пользователь неактивный, метод всегда возвращает False.
#         return self.is_admin
#
#     def has_module_perms(self, app_label):  # Возвращает True если пользователь имеет хотя бы одно право доступа
#         # для указанного приложения. Если пользователь неактивный, метод вернет False.
#         return True
#
#     username = models.CharField(unique=True, validators=[validate_username],
#                                 max_length=150)
#     email = models.EmailField(unique=True)
#     role = models.CharField(choices=ROLE_CHOICES,
#                             default='user', max_length=64)
#     bio = models.TextField()
#     first_name = models.CharField(max_length=150)
#     last_name = models.CharField(max_length=150)
#     USERNAME_FIELD = 'username'
#     REQUIRED_FIELDS = [username, email]
#
#     def __str__(self):
#         return self.email

