from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from reportlab.pdfgen import canvas
from rest_framework import mixins, renderers, status, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipe.models import (Favorite, Follow, Ingredient, Recipe, ShoppingCart,
                           Tag)
from users.models import User

from .filters import IngredientFilterContains
from .pagination import Pagination
from .serializers import (RecipeCreateSerializer,
                          RecipeIngredientReadSerializer,
                          RecipeReadlSerializer, RecipeShortSerializer,
                          TagSerializer)


class RecipeViewSet(viewsets.ModelViewSet):
    queryset = Recipe.objects.all()
    pagination_class = PageNumberPagination
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ('name',)
    ordering = ('pub_date',)

    def get_serializer_class(self):
        if self.action == 'retrieve' or self.action == 'list':
            return RecipeReadlSerializer
        elif self.action == 'shopping_cart' or self.action == 'favorite':
            return RecipeShortSerializer
        return RecipeCreateSerializer

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def get_permissions(self):
    #     if self.action == 'retrieve' or self.action == 'list':
    #         self.permission_classes = [AllowAny,]
    #     else:
    #         self.permission_classes = [IsAuthenticated,]
    #     return [permission() for permission in self.permission_classes]

    @action(detail=False, methods=['get'],
            permission_classes=[IsAuthenticated],
            )
    def download_shopping_cart(self, request):
        user = request.user
        shopping_cart = ShoppingCart.objects.filter(user=user)
        if not shopping_cart:
            return Response({'detail': 'Shopping cart is empty.'}, status=status.HTTP_404_NOT_FOUND)
        response = HttpResponse(content_type='application/pdf')
        response['Content-Disposition'] = 'attachment; filename="shopping_cart.pdf"'

        p = canvas.Canvas(response)
        p.setFont("Helvetica", 12)

        p.drawString(100, 750, "Shopping Cart:")
        p.drawString(100, 700, "User: {}".format(user.username))
        p.drawString(100, 650, "Recipes:")

        y = 600
        for item in shopping_cart:
            recipe = item.recipe
            p.drawString(120, y, recipe.name)
            y -= 20

        p.showPage()
        p.save()

        return response

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
    serializer_class = RecipeIngredientReadSerializer
    pagination_class = Pagination
    filter_backends = (DjangoFilterBackend,)
    filterset_class = IngredientFilterContains
