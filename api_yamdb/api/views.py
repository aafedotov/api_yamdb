from datetime import date

from django.db.models import Avg
from django.shortcuts import render, get_object_or_404

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, mixins, filters, permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from rest_framework_simplejwt.tokens import RefreshToken
from django.core.mail import EmailMessage
from django.contrib.auth.tokens import default_token_generator
from rest_framework.views import APIView
from rest_framework import permissions, status
from rest_framework.response import Response


from .permissions import OnlyAdminPermission, IsAdminOrReadOnly, ReadOnlyOrAuthorOrAdmin

from .serializers import CategorySerializer, CustomUserSerializer, GenreSerializer, TitleSerializer, \
    ReviewSerializer, CommentSerializer, SignUpSerializer, GetTokenSerializer, TitleReadOnlySerializer

from reviews.models import Review, Title, Genre, Category, Comment
from users.models import CustomUser
from .filters import TitleFilter


class CreateRetrieveDestroyListViewSet(mixins.CreateModelMixin,
                                       mixins.RetrieveModelMixin,
                                       mixins.DestroyModelMixin,
                                       mixins.ListModelMixin,
                                       viewsets.GenericViewSet):
    """
    Набор представлений, обеспечивающий действия `create` и `list`.
    """
    pass


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer
    pagination_class = PageNumberPagination
    permission_classes = [OnlyAdminPermission]
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)  # Поисковый бэкенд
    search_fields = ('username',)  # поля модели, по которым разрешён поиск
    lookup_field = 'username'

    def get_object(self):
        if self.kwargs['username'] == 'me':
            obj = self.request.user
            self.check_object_permissions(self.request, obj)
            return obj
        return super().get_object()


class CategoryViewSet(CreateRetrieveDestroyListViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)  # Поисковый бэкенд
    search_fields = ('name',)  # поля модели, по которым разрешён поиск
    lookup_field = 'slug'


class GenreViewSet(CreateRetrieveDestroyListViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    permission_classes = [IsAdminOrReadOnly]
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend, filters.SearchFilter)  # Поисковый бэкенд
    search_fields = ('name',)  # поля модели, по которым разрешён поиск
    lookup_field = 'slug'


class TitleViewSet(viewsets.ModelViewSet):
    # queryset = Title.objects.annotate(Avg('reviews__score'))
    queryset = Title.objects.all()
    serializer_class = TitleSerializer
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('category', 'genre', 'year', 'name')
    # filter_backends = DjangoFilterBackend
    # filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.action == 'list' or 'retrieve':
            return TitleReadOnlySerializer

        return TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [ReadOnlyOrAuthorOrAdmin]

    def get_queryset(self):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        queryset = title.reviews.all()
        return queryset

    def perform_create(self, serializer):
        title = get_object_or_404(Title, id=self.kwargs.get('title_id'))
        author = self.request.user
        serializer.save(author=author, title=title)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    pagination_class = PageNumberPagination
    permission_classes = [ReadOnlyOrAuthorOrAdmin]

    def get_queryset(self):
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        queryset = review_id.comments.all()
        return queryset

    def perform_create(self, serializer):
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review_id)

        
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

    def create(self, request, *args, **kwargs):
        """Проверяем уникальность email, меняем код 201 на 200."""
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        email = serializer.validated_data['email']
        if CustomUser.objects.filter(email=email).exists():
            return Response(
                'Такой email уже зарегистрирован.',
                status=status.HTTP_400_BAD_REQUEST
            )
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_200_OK, headers=headers
        )

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
                return Response(
                    'Неверный e-mail.', status=status.HTTP_400_BAD_REQUEST
                )
            return Response(
                'Пользователь не найден.', status=status.HTTP_404_NOT_FOUND
            )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
