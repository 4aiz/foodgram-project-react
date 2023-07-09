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


class RecipeFilter(filters.FilterSet):
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(), to_field_name='slug', method='filter_tag')
    author = filters.ModelChoiceFilter(queryset=User.objects.all())
    is_in_shopping_cart = filters.BooleanFilter(
        field_name='is_in_shopping_cart',
        method='filter_is_in_shopping_cart'
    )
    is_favorited = filters.BooleanFilter(
        field_name='is_favorited',
        method='filter_is_favorited'
    )

    def filter_tag(self, queryset, name, value):
        if value:
            tags = []
            for x in value:
                tags.append(x.slug)
            queryset = queryset.filter(tags__slug__in=tags).distinct()
        return queryset

    def filter_is_in_shopping_cart(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            queryset = queryset.filter(
                carts__user=user
            )
        return queryset

    def filter_is_favorited(self, queryset, name, value):
        user = self.request.user
        if user.is_authenticated and value:
            queryset = queryset.filter(
                favorites__user=user
            )
        return queryset

    class Meta:
        model = Recipe
        fields = ['tags', 'author', 'is_in_shopping_cart', 'is_favorited']
