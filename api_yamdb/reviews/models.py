from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import UniqueConstraint

from reviews.validators import validate_year


class Category(models.Model):
    """Модель, представляющая категории (типы) произведений."""
    name = models.CharField(max_length=256, verbose_name='категория',
                            help_text='Выберите категорию для произведения')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Genre(models.Model):
    """Модель, представляющая жанры произведений."""
    name = models.CharField(max_length=256, verbose_name='жанр',
                            help_text='Выберите жанр для произведения')
    slug = models.SlugField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Title(models.Model):
    """Произведение, на которое пишут отзывы."""
    name = models.CharField(max_length=256,
                            verbose_name='название произведения',)
    year = models.IntegerField(
        validators=[validate_year],
        verbose_name='год выпуска',
        help_text='Выберите год выпуска произведения'
    )
    category = models.ForeignKey(Category,
                                 related_name='titles',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 verbose_name='категория',
                                 help_text='Выберите категорию')
    genre = models.ManyToManyField(Genre,
                                   related_name='titles',
                                   through='GenreTitle',
                                   verbose_name='жанр',
                                   help_text='Выберите жанр для произведения')
    description = models.TextField(blank=True, null=True,
                                   verbose_name='описание произведения',
                                   help_text='Введите краткое описание'
                                   )

    def __str__(self):
        return self.name


class GenreTitle(models.Model):
    """Модель для связи произведения и жанра."""
    title = models.ForeignKey(
        Title,
        verbose_name='название произведения',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='жанр произведения',
        on_delete=models.CASCADE
    )


class Review(models.Model):
    """Отзывы пользователей о произведениях."""
    title = models.ForeignKey(
        Title, on_delete=models.CASCADE, related_name='reviews',
        verbose_name='название произведения')
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='reviews',
        verbose_name='автор')
    score = models.IntegerField(
        default=0,
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        verbose_name='оценка')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name='дата публикации')

    class Meta:
        ordering = ('-pub_date',)
        constraints = [
            UniqueConstraint(
                fields=['title', 'author'],
                name='unique_author_review'
            )
        ]

    def __str__(self):
        return self.text


class Comment(models.Model):
    review = models.ForeignKey(
        Review, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='рейтинг'
    )
    text = models.TextField(verbose_name='текст')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        related_name='comments',
        verbose_name='автор')
    pub_date = models.DateTimeField(auto_now_add=True,
                                    db_index=True,
                                    verbose_name='дата публикации')

    class Meta:
        ordering = ('-pub_date',)

    def __str__(self):
        return self.text
