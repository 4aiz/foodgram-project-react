from django.db.models import Sum, F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import mixins, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipe.models import Favorite, Ingredient, Recipe, ShoppingCart, Tag, RecipeIngredient

from .filters import IngredientFilterContains, RecipeFilter
from .pagination import Pagination
from .serializers import (IngredientSerializer, RecipeCreateSerializer,
                          RecipeReadlSerializer, RecipeShortSerializer,
                          TagSerializer)
from .permissions import IsAuthorOrReadOnly


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = RecipeFilter
    permission_classes = [AllowAny]

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return RecipeReadlSerializer
        elif self.action == 'shopping_cart' or self.action == 'favorite':
            return RecipeShortSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get_permissions(self):
        if self.action in (
                'download_shopping_cart',
                'shopping_cart',
                'favorite',
                'create',
                'update'
        ):
            return [IsAuthenticated()]
        elif self.action in ('destroy',):
            return [IsAuthorOrReadOnly()]
        elif self.action in ('list', 'retrieve'):
            return super().get_permissions()

    @action(detail=False, methods=['get'])
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = RecipeIngredient.objects.filter(
            recipe__cart__user=user).values(
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

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        if request.method == 'post':
            if ShoppingCart.objects.filter(user=user, recipe=recipe).exists():
                return Response(
                    {'detail': 'Рецепт уже в вашем списке покупок'},
                    status=status.HTTP_200_OK
                )
            else:
                ShoppingCart.objects.create(
                    user=user, recipe=recipe
                )
                return Response(
                        {'detail': 'Рецепт добавлен в список покупок'},
                        status=status.HTTP_201_CREATED
                    )

        elif request.method == 'delete':
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
                    {'detail': 'Рецепт не найден в Вашем списке покупок'},
                    status=status.HTTP_404_NOT_FOUND
                )

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user
        if Favorite.objects.filter(user=user, recipe=recipe).exists():
            return Response(
                {'detail': 'Рецепт уже в избранном'},
                status=status.HTTP_200_OK
            )

        if request.method == 'post':
            Favorite.objects.create(
                user=user, recipe=recipe
            )

        else:
            try:
                favorite = Favorite.objects.get(user=user, recipe=recipe)
                favorite.delete()
                return Response(
                    {'message': 'Рецепт удалено из избранного'},
                    status=status.HTTP_204_NO_CONTENT
                )
            except Favorite.DoesNotExist:
                return Response(
                    {'message': 'Рецепта нет в Вашем избранном'},
                    status=status.HTTP_404_NOT_FOUND
                )


class TagsViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = Pagination
    permission_classes = [AllowAny]


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilterContains
    permission_classes = [AllowAny]
