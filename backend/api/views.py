from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters, mixins

from .filters import IngredientFilterContains, IngredientFilterStartsWith
from .pagination import Pagination
from .serializers import (RecipeSerializer,
                          TagSerializer,
                          IngredientSerializer,
                          FavoriteSerializer,
                          ShoppingCartSerializer,
                          FollowSerializer)
from recipe.models import (Recipe, Ingredient, Tag, Favorite, Follow, ShoppingCart)
from users.models import User


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ('name',)
    ordering = ('name',)

    # def get_serializer_class(self):
    #     if self.action in ('create', 'partial_update'):
    #         return RecipeCreateSerializer
    #     return RecipeSerializer


class TagsViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = Pagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class IngredientViewSet(mixins.ListModelMixin,
                        mixins.RetrieveModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = Pagination
    filter_backends = (filters.SearchFilter,)
    filterset_class = (IngredientFilterContains, )
    search_fields = ('name',)
    lookup_field = 'slug'


class FavoriteViewSet(mixins.CreateModelMixin,
                      mixins.DestroyModelMixin,
                      viewsets.GenericViewSet):
    queryset = Favorite.objects.all()
    serializer_class = FavoriteSerializer

    # def get_queryset(self):
    #     user_id = self.kwargs.get('user_id')
    #     user = get_object_or_404(User, id=user_id)
    #     return user.favorites.all()


class ShoppingCartViewSet(mixins.CreateModelMixin,
                          mixins.DestroyModelMixin,
                          mixins.RetrieveModelMixin,
                          viewsets.GenericViewSet):
    queryset = ShoppingCart.objects.all()
    serializer_class = ShoppingCartSerializer


class FollowViewset(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    pagination_class = PageNumberPagination
#
#     def get_queryset(self):
#         recipe_id = self.kwargs.get('recipe_id')
#         recipe = get_object_or_404(Recipe, id=recipe_id)
#         return recipe.comments.all()
#
#     def perform_create(self, serializer):
#         title_id = self.kwargs.get('title_id')
#         recipe_id = self.kwargs.get('review_id')
#         recipe = get_object_or_404(
#             Recipe,
#             id=review_id,
#             title=title_id
#         )
#         serializer.save(author=self.request.user, review=review)
