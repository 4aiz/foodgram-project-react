import django_filters
from django_filters import rest_framework as filters
from recipe.models import Ingredient, Recipe, Tag
from users.models import User


class IngredientFilterContains(filters.FilterSet):
    """Фильтр ингредиента по началу названия"""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ('name', )


class RecipeFilter(django_filters.FilterSet):
    """Фильтр рецептов"""
    author = filters.ModelChoiceFilter(
        queryset=User.objects.all(),
        to_field_name='author__username'
    )
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        to_field_name='tags__slug'
    )
    is_in_shopping_cart = filters.BooleanFilter(field_name='is_in_shopping_cart')
    is_favorited = filters.BooleanFilter(field_name='is_favorited')

    def filter_is_in_shopping_cart(self, queryset, name, value):
        return queryset.filter(is_in_shopping_cart__isnull=False)

    def filter_is_favorited(self, queryset, name, value):
        return queryset.filter(is_favorited__isnull=False)

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_in_shopping_cart', 'is_favorited')

