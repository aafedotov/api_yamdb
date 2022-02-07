from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

from reviews.validators import validate_year


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
    year = models.IntegerField(
        validators=[validate_year],
        help_text='Select the year of release of the work'
    )
    category = models.ForeignKey(Category,
                                 related_name='titles',
                                 on_delete=models.SET_NULL,
                                 null=True,
                                 help_text='Select a category for this work')
    genre = models.ManyToManyField(Genre,
                                   related_name='titles',
                                   through='GenreTitle',
                                   help_text='Select a genre for this work')
    description = models.TextField(
        blank=True, null=True,
        help_text='Enter a brief description of the work'
    )

    def __str__(self):
        return self.name

    class Meta:
        ordering = ('-name',)


class GenreTitle(models.Model):
    """Модель для связи произведения и жанра."""
    title = models.ForeignKey(
        Title,
        verbose_name='Название произведения',
        on_delete=models.CASCADE
    )
    genre = models.ForeignKey(
        Genre,
        verbose_name='Жанр произведения',
        on_delete=models.CASCADE
    )


class Review(models.Model):
    """Отзывы пользователей о произведениях."""
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
        unique_together = ('author', 'title')

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
