from django.db.models import Avg  # может использовать из этой библиотеки
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters, mixins

from .filters import IngredientFilterContains, IngredientFilterStartsWith
from .pagination import Pagination
from .serializers import (RecipeCreateSerializer,
                          RecipeSerializer,
                          TagSerializer,
                          IngredientSerializer,
                          FollowSerializer)
from recipe.models import (Recipe, Ingredient,Tag,)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    serializer_class = RecipeSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    ordering_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return RecipeCreateSerializer
        return RecipeSerializer


class TagsViewSet(mixins.RetrieveModelMixin,
                  mixins.ListModelMixin,
                  viewsets.GenericViewSet):
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
    pagination_class = Pagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class IngredientViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    pagination_class = Pagination
    filter_backends = (filters.SearchFilter,)
    filterset_class = (IngredientFilterContains, IngredientFilterStartsWith)
    search_fields = ('name',)
    lookup_field = 'slug'


# class FollowViewset(viewsets.ModelViewSet):
#     serializer_class = FollowSerializer
#     pagination_class = PageNumberPagination
#
#     def get_queryset(self):
#         review_id = self.kwargs.get('review_id')
#         review = get_object_or_404(Review, id=review_id)
#         return review.comments.all()
#
#     def perform_create(self, serializer):
#         title_id = self.kwargs.get('title_id')
#         review_id = self.kwargs.get('review_id')
#         review = get_object_or_404(
#             Review,
#             id=review_id,
#             title=title_id
#         )
#         serializer.save(author=self.request.user, review=review)


# class ReviewViewset(viewsets.ModelViewSet):
#     serializer_class = ReviewSerializer
#     permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly, ]
#     pagination_class = PageNumberPagination
#
#     def get_queryset(self):
#         title_id = self.kwargs.get('title_id')
#         title = get_object_or_404(Title, id=title_id)
#         return title.reviews.all()
#
#     def perform_create(self, serializer):
#         title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
#         serializer.save(author=self.request.user, title=title)
