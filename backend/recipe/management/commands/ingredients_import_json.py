import os
import json
import sys

from pathlib import Path
from django.core.management.base import BaseCommand

from recipe.models import Ingredient


class Command(BaseCommand):
    def import_ingredients_from_file(self):
        data_folder = Path(__file__).resolve().parent.parent.parent.parent / 'data'
        file_path = os.path.join(data_folder, 'ingredients.json')
        with open(file_path, encoding='utf-8') as ingredients:
            data = json.load(ingredients)
            for data_object in data:
                name = data_object.get('name', None)
                measurement_unit = data_object.get('measurement_unit', None)
                Ingredient.objects.create(
                    name=name,
                    measurement_unit=measurement_unit,
                )

    def handle(self, *args, **options):
        self.import_ingredients_from_file()