from django.db import models

from users.models import User


class Tag(models.Model):
    name = models.CharField(max_length=256, db_index=True,
                            verbose_name='Имя тега',
                            help_text='Укажите имя тега')
    color = models.CharField(max_length=16)  # check this field in kittygram project in SERIALIZER
    slug = models.SlugField('Индификатор', unique=True)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    tag = models.ManyToManyField(
        Tag, verbose_name='Тэг',
        blank=True,
        related_name='recipes'
    )
    name = models.CharField(max_length=256, db_index=True,
                            verbose_name='Название блюда',
                            help_text='Укажите название блюда')
    image = models.ImageField(upload_to='recipe/images/')  # IDK NEED TO SEARCH
    description = models.TextField(blank=True, verbose_name='Описание рецепта')
    ingredients = models.CharField()  # maybe use CHOICES or something multichoices or ManyToOne field
    cooking_time = models.PositiveSmallIntegerField(verbose_name='Время готовки')

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(max_length=256, verbose_name='Ингредиент')
    count = models.PositiveSmallIntegerField(verbose_name='Количество')
    unit = models.CharField(
        max_length=256,
        verbose_name='Единица измерения',
        help_text='Укажите единицу измерения'
    )
