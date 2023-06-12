from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.pagination import PageNumberPagination
from rest_framework import viewsets, filters, mixins

from .filters import TitleFilter
from .pagination import Pagination
from .permissions import IsAuthorOrAdminOrModeratorOrReadOnly,\
    SuperuserOrAdminPermission
from .serializers import (CategoriesSerializer,
                          CommentSerializer,
                          GenresSerializer,
                          ReviewSerializer,
                          TitlesSerializer,
                          TitlesCreateSerializer
                          )
from reviews.models import (Categories,
                            Genres,
                            Title,
                            Review)


class TitlesViewSet(viewsets.ModelViewSet):
    permission_classes = [SuperuserOrAdminPermission, ]
    queryset = Title.objects.annotate(
        rating=Avg('reviews__score')).order_by('name')
    serializer_class = TitlesSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = TitleFilter
    ordering_fields = ('name',)
    ordering = ('name',)

    def get_serializer_class(self):
        if self.action in ('create', 'partial_update'):
            return TitlesCreateSerializer
        return TitlesSerializer


class GenresViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    mixins.DestroyModelMixin,
                    viewsets.GenericViewSet):
    permission_classes = [SuperuserOrAdminPermission, ]
    queryset = Genres.objects.all()
    serializer_class = GenresSerializer
    pagination_class = Pagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CategoriesViewSet(mixins.CreateModelMixin,
                        mixins.ListModelMixin,
                        mixins.DestroyModelMixin,
                        viewsets.GenericViewSet):
    permission_classes = [SuperuserOrAdminPermission, ]
    queryset = Categories.objects.all()
    serializer_class = CategoriesSerializer
    pagination_class = Pagination
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name',)
    lookup_field = 'slug'


class CommentViewset(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly, ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(Review, id=review_id)
        return review.comments.all()

    def perform_create(self, serializer):
        title_id = self.kwargs.get('title_id')
        review_id = self.kwargs.get('review_id')
        review = get_object_or_404(
            Review,
            id=review_id,
            title=title_id
        )
        serializer.save(author=self.request.user, review=review)


class ReviewViewset(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthorOrAdminOrModeratorOrReadOnly, ]
    pagination_class = PageNumberPagination

    def get_queryset(self):
        title_id = self.kwargs.get('title_id')
        title = get_object_or_404(Title, id=title_id)
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)
