from django.contrib import admin

from .models import Category, Genre, Title, Review, Comment


class TitleAdmin(admin.ModelAdmin):
    """Отображение поля many-to-many в админке."""
    list_display = ['name', 'year', 'category', 'show_genres', 'description']

    def show_genres(self, obj):
        return '\n'.join([item.name for item in obj.genre.all()])


admin.site.register(Category)
admin.site.register(Genre)
admin.site.register(Title, TitleAdmin)
admin.site.register(Review)
admin.site.register(Comment)
