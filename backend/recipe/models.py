from django.db import models

from users.models import User


CHARFIELD_LENGTH = 200


class Tag(models.Model):
    name = models.CharField(max_length=CHARFIELD_LENGTH, db_index=True,
                            verbose_name='имя тега',
                            unique=True)
    color = models.CharField(max_length=16)
    slug = models.SlugField('Индификатор', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']


class Ingredient(models.Model):
    name = models.CharField(
        max_length=CHARFIELD_LENGTH, verbose_name='название ингредиента'
    )
    measurement_unit = models.CharField(
        max_length=CHARFIELD_LENGTH,
        verbose_name='единица измерения',
        help_text='Укажите единицу измерения'
    )

    def __str__(self):
        return f'{self.name} ({self.measurement_unit})'

    class Meta:
        ordering = ['name']


class Recipe(models.Model):
    author = models.ForeignKey(
        User, verbose_name='автор',
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    tags = models.ManyToManyField(
        Tag, verbose_name='тег',
        blank=True,
        related_name='recipes'
    )
    name = models.CharField(
        max_length=CHARFIELD_LENGTH, db_index=True,
        verbose_name='название блюда',
        help_text='Укажите название блюда'
    )
    image = models.ImageField(
        upload_to='images/'
    )
    description = models.TextField(
        blank=True, verbose_name='описание рецепта'
    )
    ingredients = models.ManyToManyField(
        Ingredient, verbose_name='ингредиент',
        blank=True,
        through='RecipeIngredient',
    )
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='время готовки'
    )
    pub_date = models.DateTimeField(auto_now_add=True)
    # objects = RecipeQuerySet.as_manager()

    class Meta:
        ordering = ['-pub_date']

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE
    )
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE
    )
    amount = models.PositiveIntegerField(
        verbose_name='количество'
    )


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        verbose_name='подписчик',
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
        on_delete=models.CASCADE,
        related_name='carts'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )


class Favorite(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_user_recipe'
            )
        ]
