from django.db import migrations

INITIAL_TAGS = [
    {
        'color': '#61bdc2',
        'name': 'Основное',
        'slug': 'Main'
    },
    {
        'color': '#d1644b',
        'name': 'Перекус',
        'slug': 'Snack'
    },
    {
        'color': '#fbd37b',
        'name': 'Дессерт',
        'slug': 'Dessert'
    },
]


def add_tags(apps, schema_editor):
    Tag = apps.get_model('recipe', 'Tag')
    for tag in INITIAL_TAGS:
        new_tag = Tag(color=tag['color'], name=tag['name'], slug=tag['slug'])
        new_tag.save()


def remove_tags(apps, schema_editor):
    Tag = apps.get_model('recipe', 'Tag')
    for tag in INITIAL_TAGS:
        Tag.objects.get(slug=tag['slug']).delete()


class Migration(migrations.Migration):
    dependencies = [
        ('recipe', '0003_alter_recipe_options')
    ]

    operations = [
        migrations.RunPython(add_tags, remove_tags)
    ]
