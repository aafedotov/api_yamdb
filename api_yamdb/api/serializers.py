from datetime import date

from django.contrib.auth.validators import ASCIIUsernameValidator
from django.core.validators import validate_email
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from rest_framework.relations import SlugRelatedField
from reviews.models import Category, Genre, Title, Review, Comment
from users.models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """Сериализатор для кастомной модели пользователя."""
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
    """Сериализатор для модели категорий."""
    class Meta:
        fields = ('name', 'slug')
        model = Category

    def validate_slug(self, value):
        """Проверяем уникальность слага."""
        if Category.objects.filter(slug=value).exists():
            raise serializers.ValidationError('Slug не уникален.')
        return value


class GenreSerializer(serializers.ModelSerializer):
    """Сериализатор для модели жанров."""
    class Meta:
        fields = ('name', 'slug')
        model = Genre


class TitleReadOnlySerializer(serializers.ModelSerializer):
    """
    Сериализатор вывода списка произведений и
    получения определённого произведения.
    """
    rating = serializers.IntegerField(source='reviews__score__avg',
                                      read_only=True)
    genre = GenreSerializer(many=True)
    category = CategorySerializer()

    class Meta:
        fields = (
            'id', 'name', 'year',
            'rating', 'description',
            'genre', 'category'
        )
        model = Title

    def validate_year(self, value):
        """Проверяем валидность года выпуска."""
        year_now = date.today().year
        if value > year_now:
            raise serializers.ValidationError(
                'Год выпуска не может быть больше текущего!')
        repr(value)
        return value


class TitleSerializer(TitleReadOnlySerializer):
    """ Сериализатор создания, обновления и удаления произведений."""
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
    """Сериализатор для модели отзывов."""
    author = SlugRelatedField(slug_field='username',
                              default=serializers.CurrentUserDefault(),
                              read_only=True)
    score = serializers.IntegerField(min_value=1, max_value=10)

    def validate(self, data):
        """Проверяем, оставлял ли пользователь отзыв к произведению ранее."""
        view = self.context['view']
        request = self.context['request']
        title_id = view.kwargs.get('title_id')
        author = request.user
        if (
                Review.objects.filter(
                    author=author,
                    title__id=title_id).exists()
                and
                request.method != 'PATCH'):
            raise serializers.ValidationError(
                'Вы уже оставляли отзыв к этому произведению.'
            )
        return data

    class Meta:
        fields = ('id', 'text', 'author', 'score', 'pub_date')
        model = Review


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для модели комментариев."""
    author = SlugRelatedField(
        slug_field='username',
        read_only=True,
        default=serializers.CurrentUserDefault()
    )

    class Meta:
        fields = ('id', 'author', 'text', 'pub_date')
        model = Comment


class SignUpSerializer(serializers.Serializer):
    """Сериализатор для эндпоинта регистрации пользователей."""
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=254)

    def validate_email(self, value):
        """Проверяем валидность email."""
        try:
            validate_email(value)
        except ValidationError:
            raise serializers.ValidationError('Некорректное поле email.')
        return value

    def validate_username(self, value):
        """Проверяем валидность username."""
        if value == 'me':
            raise serializers.ValidationError(
                'Использование username -me- запрещено.'
            )
        try:
            ASCIIUsernameValidator(value)
        except ValidationError:
            raise serializers.ValidationError('Некорректное поле username.')
        return value

    def validate(self, data):
        """Проверяем наличие username и корректность email."""
        if CustomUser.objects.filter(username=data['username']).exists():
            if (
                    CustomUser.objects.get(username=data['username']).email
            ) == data['email']:
                return data
            raise serializers.ValidationError('Неверный e-mail.')
        return data


class GetTokenSerializer(serializers.ModelSerializer):
    """Сериализатор для эндпоинта получения JWT-токенов."""
    username = serializers.CharField(max_length=256)
    confirmation_code = serializers.CharField(max_length=256)

    class Meta:
        model = CustomUser
        fields = ['username', 'confirmation_code']
