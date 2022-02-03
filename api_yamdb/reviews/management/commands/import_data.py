from django.core.management.base import BaseCommand, CommandError
from .parsers.model_parsers import category_parser


class Command(BaseCommand):
    help = 'Импорт данных в БД из csv файлов.'

    def add_arguments(self, parser):
        parser.add_argument('--model', nargs='?', type=str, action='store')
        parser.add_argument('--file', nargs='?', type=str, action='store')

    def handle(self, *args, **options):
        if options['model'] == 'category':
            category_parser(options['file'])
