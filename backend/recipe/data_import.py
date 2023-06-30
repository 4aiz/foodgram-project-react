import json
import os
from pathlib import Path


INITIAL_INGREDIENTS = []


def fill_initial_data():
    data_folder = Path(__file__).resolve().parent.parent / 'data'
    file_path = os.path.join(
        data_folder, 'ingredients.json'
    )
    with open(file_path, encoding='utf-8') as ingredients:
        data = json.load(ingredients)
        for data_object in data:
            name = data_object.get('name', None)
            measurement_unit = data_object.get('measurement_unit', None)
            INITIAL_INGREDIENTS.append(
                {
                    'name': name,
                    'measurement_unit': measurement_unit
                }
            )


fill_initial_data()
