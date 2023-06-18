from django.urls import path, include
from rest_framework.authtoken import views as v
from rest_framework.authtoken import views
from rest_framework.routers import DefaultRouter


from .views import (RecipeViewSet,
                    IngredientViewSet,
                    TagsViewSet,
                    FavoriteViewSet,
                    FollowViewset,
                    ShoppingCartViewSet
                    )
from users.views import UserCreateViewSet

router = DefaultRouter()

router.register(r'recipes', RecipeViewSet, basename='recipes')
router.register(r'tags', TagsViewSet, basename='tags')
router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(
    r'^recipes/(?P<recipe_id>\d+)/favorite', FavoriteViewSet, basename='favorites'
)
router.register(r'^users/(?P<user_id>\d+)/subscribe', FollowViewset, basename='followers')
router.register(r'users/subscriptions', FollowViewset, basename='subscriptions')
router.register(r'users', UserCreateViewSet, basename='users')
router.register(r'^recipes/(?P<recipe_id>\d+)/shopping_cart', ShoppingCartViewSet, basename='shopping_cart')

app_name = 'api'

urlpatterns = [
    path('', include(router.urls)),
    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken')),
]
