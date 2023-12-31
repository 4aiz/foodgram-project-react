from django.db.models import F, Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipe.models import (Favorite, Ingredient, Recipe, RecipeIngredient,
                           ShoppingCart, Tag)
from users.serializers import RecipeShortSerializer
from .filters import IngredientFilterContains, RecipeFilter
from .pagination import Pagination, CustomLimitPagination
from .permissions import IsAdminOrReadOnly, IsAuthenticatedAuthorOrAdmin
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeReadlSerializer, TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = CustomLimitPagination
    permission_classes = [AllowAny]
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter

    def get_serializer_class(self):
        if self.action == 'shopping_cart' or self.action == 'favorite':
            return RecipeShortSerializer
        elif self.action == 'retrieve' or self.action == 'list':
            return RecipeReadlSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in (
                'download_shopping_cart',
                'shopping_cart',
                'favorite',
                'create',
        ):
            return [IsAuthenticated()]
        elif self.action in ('destroy', 'partial_update', 'update'):
            return [IsAuthenticatedAuthorOrAdmin()]
        elif self.action in ('list', 'retrieve'):
            return super().get_permissions()

    def destroy(self, request, pk):
        user = request.user
        recipe = get_object_or_404(Recipe, pk=pk, author=user)
        recipe.delete()
        return Response(
            {'detail': 'Ваш рецепт удален'},
            status=status.HTTP_204_NO_CONTENT
        )

    @action(detail=False, methods=['GET'])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = RecipeIngredient.objects.filter(
            recipe__carts__user=user).values(
            'ingredient__name',
            'ingredient__measurement_unit'
        ).annotate(
            name=F('ingredient__name'),
            unit=F('ingredient__measurement_unit'),
            amount=Sum('amount')
        )

        if not shopping_cart:
            return Response(
                {'detail': 'Корзина пуста'},
                status=status.HTTP_404_NOT_FOUND
            )

        text = '\n'.join(
            [f'{ingredient["name"]}:'
             f' {ingredient["amount"]} ({ingredient["unit"]})'
             for ingredient in shopping_cart]
        )

        response = HttpResponse(text, content_type='txt/plain')
        response['Content-Disposition'] = 'attachment;' \
                                          ' filename="shopping_cart.pdf"'

        return response

    @action(detail=True, methods=['POST', 'DELETE'])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        if request.method == 'POST':
            if ShoppingCart.objects.filter(
                    recipe__carts__recipe=recipe,
                    user=user
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже в вашем списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                ShoppingCart.objects.create(
                    user=user, recipe=recipe
                )
                return Response(
                    {'detail': 'Рецепт добавлен в список покупок'},
                    status=status.HTTP_201_CREATED
                )

        elif request.method == 'DELETE':
            try:
                shopping_cart = ShoppingCart.objects.get(
                    user=user, recipe=recipe
                )
                shopping_cart.delete()
                return Response(
                    {'detail': 'Рецепт удален из Вашего списка покупок'},
                    status=status.HTTP_204_NO_CONTENT
                )
            except ShoppingCart.DoesNotExist:
                return Response(
                    {'errors': 'Рецепт не найден в Вашем списке покупок'},
                    status=status.HTTP_400_BAD_REQUEST
                )

    @action(detail=True, methods=['POST', 'DELETE'])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, pk=pk)
        user = request.user

        if request.method == 'POST':
            if Favorite.objects.filter(
                    recipe__favorites__recipe=recipe,
                    user=user
            ).exists():
                return Response(
                    {'errors': 'Рецепт уже в избранном'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            else:
                Favorite.objects.create(
                    user=user, recipe=recipe
                )
                return Response(
                    {'detail': 'Рецепт добавлен в избранное'},
                    status=status.HTTP_201_CREATED
                )

        else:
            try:
                favorite = Favorite.objects.get(user=user, recipe=recipe)
                favorite.delete()
                return Response(
                    {'message': 'Рецепт удален из избранного'},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Favorite.DoesNotExist:
                return Response(
                    {'errors': 'Рецепта нет в Вашем избранном'},
                    status=status.HTTP_404_NOT_FOUND
                )


class TagsViewSet(viewsets.ModelViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = Pagination
    permission_classes = [IsAdminOrReadOnly]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = None
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilterContains
    permission_classes = [IsAdminOrReadOnly]
