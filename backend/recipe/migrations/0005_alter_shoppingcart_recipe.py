# Generated by Django 3.2.19 on 2023-07-02 20:52

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0004_add_tags'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shoppingcart',
            name='recipe',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, related_name='carts', to='recipe.recipe'),
        ),
    ]
