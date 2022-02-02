from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.validators import UnicodeUsernameValidator
from django.core.mail import send_mail
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


# Создаем класс менеджера пользователей
class MyUserManager(BaseUserManager):
    """Create and save a user with the given username, email and password"""

    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError('e-mail обязателен для регистрации!')
        if not username:
            raise ValueError('username обязателен для регистрации!')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
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


# Создаём свою модель User, наследуем от AbstractBaseUser
class User(AbstractBaseUser):
    """Описываем кастомную модель пользователя."""
    email = models.EmailField(unique=True, max_length=60)
    username = models.CharField(unique=True,
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
    bio = models.TextField()
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email']

    objects = MyUserManager()

    # # Посылает email пользователю. Если from_email равен None, Django использует настройку DEFAULT_FROM_EMAIL.
    # def email_user(self, subject, message, from_email=None, **kwargs):
    #     send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return True


class Category(models.Model):
    """Model representing categories (types) of works."""
    name = models.CharField(max_length=256, verbose_name='Category',
                            help_text='Select a category for this work')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Model representing genres of works."""
    name = models.CharField(max_length=256, verbose_name='Genre',
                            help_text='Select a genre for this work')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Specific work to which they write reviews."""
    name = models.CharField(max_length=256,
                            verbose_name='Title')
    year = models.IntegerField(help_text='Select the year of release of the work')
    category = models.ForeignKey(Category,
                                 related_name='titles',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 help_text='Select a category for this work')
    genre = models.ManyToManyField(Genre,
                                   related_name='titles',
                                   help_text='Select a genre for this work')
    description = models.TextField(blank=True, null=True,
                                   help_text='Enter a brief description of the work')

    def __str__(self):
        return self.name


class Review(models.Model):
    """User reviews for works."""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews')
    text = models.TextField(verbose_name='Text')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='Author')
    score = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='Rating')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name='Publication date')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE, related_name='comments')
    text = models.TextField(verbose_name='Текст')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name="comments",
        verbose_name='Author')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name='Publication date')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
