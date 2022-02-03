import csv
import os
from django.conf import settings

from reviews.models import Genre


def category_parser(file):
    file_path = os.path.join(settings.BASE_DIR, file)
    with open(file_path, newline='') as f:
        reader = csv.reader(f)
        for row in reader:
            print(row)