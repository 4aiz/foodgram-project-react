from django_filters import rest_framework as filters

from recipe.models import Ingredient


class IngredientFilterContains(filters.FilterSet):
    """Фильтр ингредиента по началу названия"""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ['name']


class RecipeFilter(filters.FilterSet):
    """Фильтр рецептов по тегам"""
    pass

