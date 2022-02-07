import csv
import os

from django.conf import settings
from reviews.models import Genre, Category, Title, Comment, GenreTitle, Review
from users.models import CustomUser


def csv_parser(file):
    """Выносим общий для всех парсеров функционал по csv."""
    file_path = os.path.join(settings.BASE_DIR, file)
    result = []
    with open(file_path, newline='', encoding='utf-8') as f:
        reader = csv.reader(f)
        next(reader)
        for row in reader:
            result.append(row)
    return result


def category_parser(file):
    """Парсер для модели категорий."""
    rows = csv_parser(file)
    objs = [
        Category(
            name=row[1],
            slug=row[2],
        )
        for row in rows
    ]
    Category.objects.bulk_create(objs)


def genre_parser(file):
    """Парсер для модели жанров."""
    rows = csv_parser(file)
    objs = [
        Genre(
            name=row[1],
            slug=row[2],
        )
        for row in rows
    ]
    Genre.objects.bulk_create(objs)


def title_parser(file):
    """Парсер для модели тайтлов."""
    rows = csv_parser(file)
    objs = [
        Title(
            name=row[1],
            year=row[2],
            category_id=row[3]
        )
        for row in rows
    ]
    Title.objects.bulk_create(objs)


def genre_title_parser(file):
    """Парсер для промежуточной модели тайтлов и жанров."""
    rows = csv_parser(file)
    objs = [
        GenreTitle(
            title_id=row[1],
            genre_id=row[2],
        )
        for row in rows
    ]
    GenreTitle.objects.bulk_create(objs)


def review_parser(file):
    """Парсер для модели отзывов."""
    rows = csv_parser(file)
    objs = [
        Review(
            title_id=row[1],
            text=row[2],
            author_id=row[3],
            score=row[4],
            pub_date=row[5]
        )
        for row in rows
    ]
    Review.objects.bulk_create(objs)


def custom_user_parser(file):
    """Парсер для модели пользователей."""
    rows = csv_parser(file)
    objs = [
        CustomUser(
            id=row[0],
            username=row[1],
            email=row[2],
            role=row[3],
            bio=row[4],
            first_name=row[5],
            last_name=row[6]
        )
        for row in rows
    ]
    CustomUser.objects.bulk_create(objs)


def comment_parser(file):
    """Парсер для модели комментариев."""
    rows = csv_parser(file)
    objs = [
        Comment(
            review_id=row[1],
            text=row[2],
            author_id=row[3],
            pub_date=row[4]
        )
        for row in rows
    ]
    Comment.objects.bulk_create(objs)
