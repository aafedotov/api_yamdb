from django.contrib import admin

from .models import Category, Comment, Genre, Review, Title


class CategoryAdmin(admin.ModelAdmin):
    """Администрирование категорий."""
    list_display = ['name', 'slug']
    list_filter = ['slug']
    search_fields = ['name', 'slug']
    ordering = ['name']
    empty_value_display = '-пусто-'


class GenreAdmin(admin.ModelAdmin):
    """Администрирование жанров."""
    list_display = ['name', 'slug']
    list_filter = ['slug']
    search_fields = ['name', 'slug']
    ordering = ['name']
    empty_value_display = '-пусто-'


class TitleAdmin(admin.ModelAdmin):
    """
    Администрирование произведений.
    """
    list_display = ['name', 'year', 'description', 'category', 'show_genres']
    list_filter = ['name', 'year', 'category', 'genre']
    search_fields = ['name', 'year', 'category', 'genre']
    ordering = ['name', '-year']
    empty_value_display = '-пусто-'

    def show_genres(self, obj):
        return '\n'.join([item.name for item in obj.genre.all()])


class ReviewAdmin(admin.ModelAdmin):
    """
    Администрирование отзывов.
    """
    list_display = ['title', 'text', 'author', 'score', 'pub_date']
    list_filter = ['title', 'score']
    search_fields = ['title', 'author']
    ordering = ['title']
    empty_value_display = '-пусто-'


class CommentAdmin(admin.ModelAdmin):
    """
    Администрирование комментариев.
    """
    list_display = ('text', 'author', 'pub_date')
    list_filter = ['author']
    search_fields = ['author']
    empty_value_display = '-пусто-'


admin.site.register(Category, CategoryAdmin)
admin.site.register(Genre, GenreAdmin)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Comment, CommentAdmin)
