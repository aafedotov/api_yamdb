from django.shortcuts import render, get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters, permissions, status
from rest_framework.pagination import PageNumberPagination

from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response


from .serializers import CategorySerializer, CustomUserSerializer, GenreSerializer, TitleSerializer, \
    ReviewSerializer, CommentSerializer, SignUpSerializer, GetTokenSerializer, TitleReadOnlySerializer

from reviews.models import Review, Title, Genre, Category, Comment
from users.models import CustomUser
from .filters import TitleFilter


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    # pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)  # Поисковый бэкенд
    search_fields = ('username',)  # поля модели, по которым разрешён поиск
    lookup_field = 'username'


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)  # Поисковый бэкенд
    search_fields = ('name',)  # поля модели, по которым разрешён поиск
    lookup_field = 'slug'


class GenreViewSet(viewsets.ModelViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)  # Поисковый бэкенд
    search_fields = ('name',)  # поля модели, по которым разрешён поиск
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    # filter_backends = DjangoFilterBackend
    # filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'list':
            return TitleReadOnlySerializer

        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title_id.reviews.all()
        return new_queryset

    def perform_create(self, serializer):  # нужно сохранять текущего юзера и конкретный отзыв
        title_id = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):  # нужны не все комменты, а только связанные с конкретным отзывом с id=review_id
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review_id.comments.all()
        return new_queryset

    def perform_create(self, serializer):  # нужно сохранять текущего юзера и конкретный отзыв
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review_id)



class SignUpUserViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):

    """View-set: Регистрация пользователей."""

    serializer_class = SignUpSerializer
    permission_classes = [permissions.AllowAny]
    queryset = CustomUser.objects.all()
    
    @staticmethod
    def send_confirmation_code(user, to_email):
        mail_subject = 'Email confirmation. YamDb.'
        token = default_token_generator.make_token(user)
        message = (
                'Для завершения регистрации подтвердите Ваш email.' +
                f'\nToken:{token}'
        )
        email = EmailMessage(
            mail_subject, message, to=[to_email]
        )
        email.send()

    def perform_create(self, serializer):
        if serializer.is_valid():
            user, created = CustomUser.objects.get_or_create(
                username=serializer.validated_data['username'],
                email=serializer.validated_data['email']
            )
            to_email = serializer.validated_data['email']
            if created:
                user.is_active = False
                user.save()
                SignUpUserViewSet.send_confirmation_code(user, to_email)
                return Response(serializer.data, status.HTTP_200_OK)
            else:
                SignUpUserViewSet.send_confirmation_code(user, to_email)
                return Response(serializer.data, status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTokenApiView(APIView):
    """Получение JWT токена."""
    permission_classes = [permissions.AllowAny]

    def post(self, request):

        serializer = GetTokenSerializer(data=request.data)

        if serializer.is_valid():
            username = serializer.validated_data['username']
            confirmation_code = serializer.validated_data['confirmation_code']
            if CustomUser.objects.filter(username=username).exists():
                user = CustomUser.objects.get(username=username)
                if default_token_generator.check_token(user, confirmation_code):
                    access_token = RefreshToken.for_user(user).access_token
                    user.is_active = True
                    user.save()
                    data = {"token": str(access_token)}
                    return Response(data, status=status.HTTP_200_OK)
            return Response('Пользователь не найден', status=status.HTTP_404_NOT_FOUND)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)