from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


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
