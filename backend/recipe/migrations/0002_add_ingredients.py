from django.db import migrations
from recipe.data_import import INITIAL_INGREDIENTS


def add_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('recipe', 'Ingredient')
    for ingredient in INITIAL_INGREDIENTS:
        new_ingredient = Ingredient(
            name=ingredient['name'],
            measurement_unit=ingredient['measurement_unit'],
        )
        new_ingredient.save()


def remove_ingredients(apps, schema_editor):
    Ingredient = apps.get_model('recipe', 'Ingredient')
    for ingredient in INITIAL_INGREDIENTS:
        Ingredient.objects.get(
            name=ingredient['name'],
            measurement_unit=ingredient['measurement_unit']
        ).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_ingredients,
            remove_ingredients
        )
    ]
