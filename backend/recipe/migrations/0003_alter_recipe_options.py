# Generated by Django 3.2.19 on 2023-06-29 22:25

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0002_add_ingredients'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date']},
        ),
    ]
