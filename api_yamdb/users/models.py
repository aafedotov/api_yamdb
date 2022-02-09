from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models

from .validators import validate_username


class CustomUserManager(BaseUserManager):
    """Описываем кастомную модель пользователя."""

    def create_user(self, email, username, role='', bio='', password=None):
        if not email:
            raise ValueError('e-mail обязателен для регистрации!')
        if not username:
            raise ValueError('username обязателен для регистрации!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
            bio=bio,
            role=role
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(
            self, email, username, password, role='admin', bio=''
    ):
        user = self.create_user(
            email=self.normalize_email(email),
            password=password,
            username=username,
        )
        user.role = role
        user.bio = bio
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class UserRole:
    """Определяем роли пользователей."""

    USER = 'user'
    MODERATOR = 'moderator'
    ADMIN = 'admin'


class CustomUser(AbstractBaseUser):
    """Описываем кастомную модель пользователя."""
    email = models.EmailField(unique=True, max_length=254,
                              verbose_name='email')
    username = models.CharField(unique=True,
                                validators=[validate_username],
                                max_length=150,
                                verbose_name='имя пользователя')
    date_joined = models.DateTimeField(verbose_name='дата создания',
                                       auto_now_add=True)
    last_login = models.DateTimeField(verbose_name='последний вход в систему',
                                      auto_now=True)
    is_admin = models.BooleanField(default=False,
                                   verbose_name='Администратор')
    is_active = models.BooleanField(default=True,
                                    verbose_name='активный')
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False,
                                       verbose_name='Суперпользователь')

    ROLE_CHOICES = (
        (UserRole.USER, 'Аутентифицированный пользователь'),
        (UserRole.MODERATOR, 'Модератор'),
        (UserRole.ADMIN, 'Администратор')
    )
    role = models.CharField(choices=ROLE_CHOICES,
                            default='user', max_length=64,
                            verbose_name='role',)
    bio = models.TextField(blank=True, verbose_name='о себе')
    first_name = models.CharField(max_length=150, blank=True,
                                  verbose_name='имя')
    last_name = models.CharField(max_length=150, blank=True,
                                 verbose_name='фамилия')

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = CustomUserManager()

    @property
    def is_user(self):
        """Описываем свойства для пермишенов."""
        return self.role == UserRole.USER

    @property
    def is_admin_or_superuser(self):
        """Описываем свойства для пермишенов."""
        return self.role == UserRole.ADMIN or self.is_superuser

    @property
    def is_admin_or_moderator(self):
        """Описываем свойства для пермишенов."""
        return (self.role in (UserRole.ADMIN, UserRole.MODERATOR)
                or self.is_superuser)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True
