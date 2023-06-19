from django.db import models
from django.utils.text import slugify

from users.models import User


# COLORS = {
#     'Завтрак': '#E26C2D',
#     'Обед': '#49B64E',
#     'Ужин': '#8775D2'
# }


class Tag(models.Model):
    name = models.CharField(max_length=256, db_index=True,
                            verbose_name='Имя тега',
                            unique=True)
    color = models.CharField(max_length=16)
    slug = models.SlugField('Индификатор', unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Ingredient(models.Model):
    name = models.CharField(
        max_length=200, verbose_name='Название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=200,
        verbose_name='Единица измерения',
        help_text='Укажите единицу измерения'
    )

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name='Автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='Тег',
        blank=True,
        related_name='recipes'
    )
    name = models.CharField(
        max_length=256, db_index=True,
        verbose_name='Название блюда',
        help_text='Укажите название блюда'
    )
    image = models.ImageField(
        upload_to='images/'
    )
    description = models.TextField(
        blank=True, verbose_name='Описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name='Ингредиент',
        blank=True,
        related_name='recipes',
        through='RecipeIngredient',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время готовки'
    )

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.DO_NOTHING
    )
    amount = models.PositiveIntegerField(
        verbose_name='Количество'
    )

    def __str__(self):
        return self.ingredient


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='following',
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'following'],
                name='unique_user_following'
            )
        ]


class ShoppingCart(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.DO_NOTHING,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING
    )
