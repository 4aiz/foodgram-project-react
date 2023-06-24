from django_filters import rest_framework as filters


from recipe.models import Ingredient


class IngredientFilterContains(filters.FilterSet):
    """Имя ингредиента начинается на запрос"""
    name = filters.CharFilter(
        field_name='name',
        lookup_expr='istartswith'
    )

    class Meta:
        model = Ingredient
        fields = ['name']


# class IngredientFilter(filters.FilterSet):
#     name = filters.CharFilter(
#         field_name='name',
#         lookup_expr='istartswith'
#     )
#     name_contains = filters.CharFilter(
#         field_name='name',
#         lookup_expr='icontains'
#     )
#
#     class Meta:
#         model = Ingredient
#         fields = ['name']

