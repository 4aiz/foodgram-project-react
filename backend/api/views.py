from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, mixins, status, renderers
from rest_framework.response import Response

from .filters import IngredientFilterContains
from .pagination import Pagination
from .serializers import (RecipeDetailSerializer,
                          RecipeCreateSerializer,
                          TagSerializer,
                          IngredientSerializer,
                          FavoriteSerializer,
                          ShoppingCartSerializer,
                          FollowSerializer)
from recipe.models import (Recipe, Ingredient, Tag, Favorite, Follow, ShoppingCart)
from users.models import User


class PassthroughRenderer(renderers.BaseRenderer):
    """
        Return data as-is. View should supply a Response.
    """
    media_type = ''
    format = ''

    def render(self, data, accepted_media_type=None, renderer_context=None):
        return data


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeDetailSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    ordering = ('pub_date',)

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list' or self.action == 'put':
            return RecipeDetailSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_permissions(self):
    #     if self.action == 'retrieve' or self.action == 'list':
    #         self.permission_classes = [AllowAny,]
    #     else:
    #         self.permission_classes = [IsAuthenticated,]
    #     return [permission() for permission in permission_classes]

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated],
            renderer_classes=(PassthroughRenderer,)
            )
    def download_shopping_cart(self, request):
        pass

    @action(detail=True, methods=['post', 'delete'])
    def shopping_cart(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        if request.method == 'POST':
            shopping_cart, created = ShoppingCart.objects.get_or_create(user=user, recipe=recipe)

            if created:
                return Response({'message': 'Recipe added to shopping cart.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Recipe is already in the shopping cart.'}, status=status.HTTP_200_OK)
        else:
            try:
                shopping_cart = ShoppingCart.objects.get(user=user, recipe=recipe)
                shopping_cart.delete()
                return Response({'message': 'Recipe removed from shopping cart.'}, status=status.HTTP_204_NO_CONTENT)
            except ShoppingCart.DoesNotExist:
                return Response({'message': 'Recipe is not in the shopping cart.'}, status=status.HTTP_404_NOT_FOUND)

    @action(detail=True, methods=['post', 'delete'])
    def favorite(self, request, pk):
        recipe = get_object_or_404(Recipe, id=pk)
        user = request.user

        favorite, created = Favorite.objects.get_or_create(user=user, recipe=recipe)
        if request.method == 'POST':

            if created:
                return Response({'message': 'Recipe added to favorites.'}, status=status.HTTP_201_CREATED)
            else:
                return Response({'message': 'Recipe is already in the favorites.'}, status=status.HTTP_200_OK)
        else:
            try:
                favorite = Favorite.objects.get(user=user, recipe=recipe)
                favorite.delete()
                return Response({'message': 'Recipe removed from favorite list.'}, status=status.HTTP_204_NO_CONTENT)
            except Favorite.DoesNotExist:
                return Response({'message': 'Recipe is not in the favorite list.'}, status=status.HTTP_404_NOT_FOUND)


class TagsViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = Pagination


class IngredientViewSet(viewsets.ModelViewSet):
    queryset = Ingredient.objects.all()
    pagination_class = PageNumberPagination
    serializer_class = IngredientSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilterContains


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer


class ShoppingCartViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer


class FollowViewset(mixins.CreateModelMixin,
                    mixins.DestroyModelMixin,
                    mixins.RetrieveModelMixin,
                    viewsets.GenericViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
