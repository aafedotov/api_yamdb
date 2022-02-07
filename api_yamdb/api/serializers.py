from django.db.models import Avg
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField

from reviews.models import Category, Genre, Title, Review, Comment
from users.models import CustomUser
from datetime import date


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        ]
        model = CustomUser


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Category


class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadOnlySerializer(serializers.ModelSerializer):  # для get
    """
    Сериализатор вывода списка произведений и
    получения определённого произведения.
    """
    # rating = serializers.IntegerField(
    #     source='reviews__score__avg', read_only=True
    # )

    rating = serializers.SerializerMethodField(read_only=True)  # создать новое поле(нет в мод Title),связанное методом get_rating
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    # name = serializers.ReadOnlyField(source='title_id')

    class Meta:
        fields = (
            'id', 'name', 'year',
            'rating', 'description',
            'genre', 'category'
        )
        model = Title

    def get_rating(self, title):
        return Review.objects.filter(title_id=title.id).annotate(Avg('reviews__score'))

    def validate_year(self, value):
        year_now = date.today().year
        if value > year_now:
            raise serializers.ValidationError('Год выпуска не может быть больше текущего!')
        repr(value)
        return value


class TitleSerializer(serializers.ModelSerializer):
    """ Сериализатор создания, частичного обновления и удаления произведений."""
    genre = serializers.SlugRelatedField(
        slug_field='slug', many=True, queryset=Genre.objects.all()
    )
    category = serializers.SlugRelatedField(
        slug_field='slug', queryset=Category.objects.all()
    )

    class Meta:
        fields = ('id', 'name', 'year',
                  'description', 'genre', 'category')
        model = Title


class ReviewSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True)  # переопред поле author д/отража не id автора, его username.
    score = serializers.IntegerField(min_value=1, max_value=10)

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username',
                              read_only=True)  # переопред поле author д/отража не id автора, его username.

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment


class SignUpSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=30)
    email = serializers.CharField(max_length=60)

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'Использование username -me- запрещено.'
            )
        return value

    def validate(self, data):
        if CustomUser.objects.filter(username=data['username']).exists():
            if (
                    CustomUser.objects.get(username=data['username']).email
            ) == data['email']:
                return data
            raise serializers.ValidationError('Неверный e-mail.')
        return data


class GetTokenSerializer(serializers.ModelSerializer):
    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=256)

    class Meta:
        model = CustomUser
        fields = ['username', 'confirmation_code']
