import django_filters

from recipe.models import Ingredient


class IngredientFilterContains(django_filters.FilterSet):
    """Фильтр по ингредиентам"""
    ingredient = django_filters.CharFilter(
        field_name='name',
        lookup_expr='icontains'
    )

    class Meta:
        model = Ingredient
        fields = '__all__'


class IngredientFilterStartsWith(django_filters.FilterSet):
    ingredient = django_filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = '__all__'
