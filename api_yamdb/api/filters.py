from django_filters import rest_framework as filters

from reviews.models import Title


class TitleFilter(filters.FilterSet):
    category = filters.CharFilter(field_name='category__slug',  # field_name: имя поля модели для фильтрации.
                                  lookup_expr='icontains')  # Поиск поля для использования при фильтрации
    genre = filters.CharFilter(field_name='genre__slug',
                               lookup_expr='icontains')
    year = filters.CharFilter(field_name='year', lookup_expr='icontains')
    name = filters.CharFilter(field_name='name', lookup_expr='icontains')

    class Meta:
        model = Title
        fields = ['category', 'genre', 'year', 'name']
