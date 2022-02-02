from django.shortcuts import render, get_object_or_404
from rest_framework import viewsets

from .serializers import CategorySerializer, CustomUserSerializer, GenreSerializer, TitleSerializer, \
    ReviewSerializer, CommentSerializer
from ..reviews.models import Review, Title
from ..users.models import CustomUser


class CustomUserViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CustomUserSerializer


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = CategorySerializer


class GenreViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = GenreSerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = CustomUser.objects.all()
    serializer_class = TitleSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer

    def get_queryset(self):
        title_id = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        new_queryset = title_id.reviews.all()
        return new_queryset

    def perform_create(self, serializer):  # нужно сохранять текущего юзера и конкретный отзыв
        title_id = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, review_id=title_id)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer

    def get_queryset(self):  # нужны не все комменты, а только связанные с конкретным отзывом с id=review_id
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        new_queryset = review_id.comments.all()
        return new_queryset

    def perform_create(self, serializer):  # нужно сохранять текущего юзера и конкретный отзыв
        review_id = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review_id=review_id)
