from django.core.management.base import BaseCommand
from .parsers.model_parsers import (
    category_parser, genre_parser, comment_parser, title_parser, review_parser,
    genre_title_parser, custom_user_parser
)


class Command(BaseCommand):
    help = 'Импорт данных в БД из csv файлов.'

    def add_arguments(self, parser):
        parser.add_argument('--model', nargs='?', type=str, action='store')
        parser.add_argument('--file', nargs='?', type=str, action='store')

    def handle(self, *args, **options):
        if options['model'] == 'category':
            category_parser(options['file'])
        if options['model'] == 'genre':
            genre_parser(options['file'])
        if options['model'] == 'title':
            title_parser(options['file'])
        if options['model'] == 'comment':
            comment_parser(options['file'])
        if options['model'] == 'review':
            review_parser(options['file'])
        if options['model'] == 'genre-title':
            genre_title_parser(options['file'])
        if options['model'] == 'custom-user':
            custom_user_parser(options['file'])
