from django.core.management.base import BaseCommand

from .parsers.model_parsers import (
    category_parser, genre_parser, comment_parser, title_parser, review_parser,
    genre_title_parser, custom_user_parser
)


class Command(BaseCommand):
    help = 'Импорт данных в БД из csv файлов.'

    HANDLERS = {
        'category': category_parser,
        'genre': genre_parser,
        'title': title_parser,
        'comment': comment_parser,
        'review': review_parser,
        'genre-title': genre_title_parser,
        'custom-user': custom_user_parser
    }

    def add_arguments(self, parser):
        parser.add_argument('--model', nargs='?', type=str, action='store')
        parser.add_argument('--file', nargs='?', type=str, action='store')

    def handle(self, *args, **options):
        Command.HANDLERS[options['model']](options['file'])
